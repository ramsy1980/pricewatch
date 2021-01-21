from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User, errors, requires_login

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.register(name, email, password)
            user.send_email_verification()
            flash("An email has been sent. \
                  Please check your inbox and confirm your email address to enable notifications.",
                  category="green"
                  )

            session['email'] = user.email
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

            return redirect(url_for('alerts.index'))
        except errors.UserError as e:
            flash(e.message, 'red')
            return redirect(url_for('.login_user'))

    return render_template('/users/login.html')


@user_blueprint.route('/profile', methods=["GET", "POST"])
@requires_login
def user_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone-number']

        try:
            print(name, email, password, phone_number)

            return redirect(url_for('.user_profile'))
        except errors.UserError as e:
            flash(e.message, 'red')
            return redirect(url_for('.user_profile'))

    user = User.find_by_email(session['email'])
    if not user.is_email_verified():
        flash('Unable to send alerts. Your email address is not verified.', 'yellow')

    return render_template('/users/profile.html', user=user)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('.login_user'))
