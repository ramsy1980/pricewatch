import phonenumbers
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models.user import User, requires_login

phone_number_blueprint = Blueprint('phone-numbers', __name__)


@phone_number_blueprint.route('/verify', methods=["GET", "POST"])
@requires_login
def verify_phone_number():
    user = User.find_by_email(session['email'])

    num = phonenumbers.parse(f"{session['country_code']}{session['national_number']}", None)
    phone_number = f"+{num.country_code}{num.national_number}"

    user.send_phone_number_verification(phone_number)

    if request.method == "POST":
        verification_code = request.form['verification_code']

        if user.verify_phone_number_verification(phone_number, verification_code):
            flash("You have successfully verified your phone number", "green")
            if user.credits_available == 0:
                return redirect(url_for('credits.index'))
            else:
                return redirect(url_for('alerts.index'))
        else:
            flash("Unable to verify your phone number", "red")
            return redirect(url_for('.verify_phone_number'))

    return render_template('/phone-numbers/verify.html')

