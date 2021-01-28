from flask import Blueprint, render_template, session, flash, url_for
from pricewatch.models import User, requires_login, Payment, Notification
from pricewatch.common import DisplayFlashMessages

credit_blueprint = Blueprint('credits', __name__)


@credit_blueprint.route('/')
@requires_login
def index():
    user = User.find_by_email(session['email'])
    payments = Payment.find_many_by("user_id", user.id)
    notifications = Notification.find_many_by("user_id", user.id)

    if user.is_email_verified() and user.phone_number == "":
        DisplayFlashMessages.phone_number_not_verified()

    return render_template('/credits/index.html', user=user, payments=payments, notifications=notifications, active="credits")


@credit_blueprint.route('/add')
@requires_login
def add_credits():
    return render_template('/credits/add.html')

