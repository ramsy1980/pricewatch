import os
import phonenumbers
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models.user import User, errors, requires_login
from src.common import Utils, DisplayFlashMessages, logger

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.register(name=name, email=email, password=password)
            user.send_email_verification()
            flash("An email has been sent. \
                  Please check your inbox and confirm your email address to enable notifications.",
                  category="green"
                  )

            session['email'] = user.email
            session['is_admin'] = os.environ.get('ADMIN_EMAIL') == user.email

            return redirect(url_for('alerts.index'))
        except errors.UserError as e:
            flash(e.message, 'red')
            return render_template('/users/register.html', name=name, email=email, password=password)

    return render_template('/users/register.html')


@user_blueprint.route('/login', methods=["GET", "POST"])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.is_login_valid(email, password)
            session['email'] = email
            session['is_admin'] = os.environ.get('ADMIN_EMAIL') == email

            return redirect(url_for('alerts.index'))
        except errors.UserError as e:
            flash(e.message, 'red')
            return redirect(url_for('.login_user'))

    return render_template('/users/login.html')


@user_blueprint.route('/profile', methods=["GET", "POST"])
@requires_login
def user_profile():
    user = User.find_by_email(session['email'])

    if user.is_email_verified() and user.phone_number == "":
        DisplayFlashMessages.phone_number_not_verified()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        country_code = request.form['country-code']
        national_number = request.form['national-number']

        try:
            has_changes = False

            if password != "****" and not Utils.verify_hashed_password(password, user.password):
                user.password = Utils.hash_password(password)
                has_changes = True

            if name != user.name:
                user.name = name
                has_changes = True

            if has_changes:
                logger.info("Saving User changes ...")
                user.save_to_db()

            if f"{country_code}{national_number}" != user.phone_number:
                logger(country_code, national_number, f"{country_code}{national_number}", user.phone_number, national_number != "" or f"{country_code}{national_number}" != user.phone_number)
                session['country_code'] = country_code
                session['national_number'] = national_number

                return redirect(url_for('phone-numbers.verify_phone_number'))

            return redirect(url_for('.user_profile'))
        except errors.UserError as e:
            flash(e.message, 'red')
            return redirect(url_for('.user_profile'))

    if not user.is_email_verified():
        flash('Unable to send alerts. Your email address is not verified.', 'yellow')

    phone_number = phonenumbers.parse(user.phone_number, None) if user.phone_number != "" else None
    return render_template('/users/profile.html', user=user, phone_number=phone_number, active="profile")


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    session['is_admin'] = None
    return redirect(url_for('.login_user'))
