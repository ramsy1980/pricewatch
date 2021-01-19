from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User, errors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register(email, password)
            session['email'] = email

            return redirect(url_for('alerts.index'))
        except errors.UserError as e:
            flash(e.message, 'danger')
            return redirect(url_for('.register_user'))

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
            flash(e.message, 'danger')
            return redirect(url_for('.login_user'))

    return render_template('/users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('.login_user'))
