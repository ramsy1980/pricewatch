from flask import Blueprint, render_template, request, redirect, url_for, session
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

            return email
        except errors.UserError as e:
            return e.message

    return render_template('/users/register.html')
