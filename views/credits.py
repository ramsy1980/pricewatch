from flask import Blueprint, render_template, session, flash, url_for
from models.user import User, requires_login
from models.payment import Payment
from models.notification import Notification

credit_blueprint = Blueprint('credits', __name__)


@credit_blueprint.route('/')
@requires_login
def index():
    user = User.find_by_email(session['email'])
    payments = Payment.find_many_by("user_id", user.id)
    notifications = Notification.find_many_by("user_id", user.id)
    print("payments", payments)
    link = f"<a href='{url_for('users.user_profile')}' class='underline'>update</a>"
    if user.phone_number == "":
        flash(f"Unable to send SMS notifications. Please {link} your phone number first", "yellow")
    return render_template('/credits/index.html', user=user, payments=payments, notifications=notifications)


@credit_blueprint.route('/add')
@requires_login
def add_credits():
    return render_template('/credits/add.html')

