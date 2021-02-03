import os
import stripe
import schedule
from datetime import datetime
from flask import Flask, render_template, jsonify, session, request, redirect, url_for
from src.models import Payment, User, requires_login, errors
from src.views import alert_blueprint, store_blueprint, user_blueprint, email_blueprint, phone_number_blueprint, \
    credit_blueprint, payment_blueprint, link_blueprint
from src.common import DisplayFlashMessages, logger
from src.models.alert import Alert

APP_DOMAIN_URL = os.environ.get('APP_DOMAIN_URL')
APP_SECRET = os.environ.get('APP_SECRET')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')

if APP_DOMAIN_URL is None:
    raise RuntimeError("Failed to load APP_DOMAIN_URL")
if APP_SECRET is None:
    raise RuntimeError("Failed to load APP_SECRET")
if ADMIN_EMAIL is None:
    raise RuntimeError("Failed to load ADMIN_EMAIL")
if STRIPE_SECRET_KEY is None:
    raise RuntimeError("Failed to load STRIPE_SECRET_KEY")
if STRIPE_PUBLISHABLE_KEY is None:
    raise RuntimeError("Failed to load STRIPE_PUBLISHABLE_KEY")
if STRIPE_ENDPOINT_SECRET is None:
    raise RuntimeError("Failed to load STRIPE_ENDPOINT_SECRET")

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)
app.secret_key = APP_SECRET
app.template_folder = "src/templates"

app.config.update(
    ADMIN_EMAIL=ADMIN_EMAIL,
    APP_DOMAIN_URL=APP_DOMAIN_URL
)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['country_code'] = request.form['country-code']
        session['national_number'] = request.form['national-number']

        return redirect(url_for('phone-numbers.verify_phone_number'))

    try:
        email = session.get('email', None)
        user = User.find_by_email(email)
        if user.is_email_verified() and user.phone_number == "":
            DisplayFlashMessages.phone_number_not_verified()
    except errors.UserNotFoundError:
        user = None

    return render_template('home.html', user=user, active="home")


app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(email_blueprint, url_prefix="/emails")
app.register_blueprint(phone_number_blueprint, url_prefix="/phone-numbers")
app.register_blueprint(credit_blueprint, url_prefix="/credits")
app.register_blueprint(payment_blueprint, url_prefix="/payments")
app.register_blueprint(link_blueprint, url_prefix="/links")


@app.route("/config", methods=["POST"])
@requires_login
def get_publishable_key():
    stripe_config = {"publicKey": STRIPE_PUBLISHABLE_KEY}
    return jsonify(stripe_config)


@app.route("/create-checkout-session", methods=["POST"])
@requires_login
def create_checkout_session():
    stripe.api_key = STRIPE_SECRET_KEY
    user = User.find_by_email(session['email'])
    customer = stripe.Customer.list(email=user.email, limit=1).data[0] or stripe.Customer.create(
        name=user.name,
        email=user.email,
    )

    success_uri = request.args.get('success_uri', "/payments/success?session_id={CHECKOUT_SESSION_ID}")

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=user.id,
            success_url=APP_DOMAIN_URL + success_uri,
            cancel_url=APP_DOMAIN_URL + "/payments/cancelled",
            payment_method_types=["ideal", "card", "bancontact", "eps", "giropay", "sofort"],
            mode="payment",
            customer=customer,
            line_items=[
                {
                    "name": "PriceWatch: 5 SMS credits",
                    "quantity": 5,
                    "currency": "eur",
                    "amount": "100",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        logger.info("Payment was successful.")
        user_id = event.data['object']['client_reference_id']
        payment_intent_id = event.data['object']['payment_intent']

        user = User.get_by_id(user_id)

        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        created = datetime.fromtimestamp(payment_intent.created)
        amount = int(payment_intent.amount / 100)

        payment = Payment(_id=payment_intent_id, amount=amount, created=created, user_id=user.id)
        logger.info("Payment added", payment)
        payment.save_to_db()

        user.total_credits += amount
        user.save_to_db()

    return "Success", 200


def send_alerts():
    alerts = Alert.all()

    for alert in alerts:
        alert.load_item_price()
        alert.notify_if_price_reached()

    if not alerts:
        logger.info("No alerts have been created. Create an alert to get started.")


if __name__ == '__main__':
    schedule.every(1).minute.do(send_alerts)
    app.run(host='0.0.0.0', debug=True)
