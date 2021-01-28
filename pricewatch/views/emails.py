from flask import Blueprint, redirect, url_for, session, flash
from pricewatch.models.user import User, errors

email_blueprint = Blueprint('emails', __name__)


@email_blueprint.route('/verify/<string:email_verification_token>')
def verify_email(email_verification_token):
    try:
        user = User.find_by_email_verification_token(email_verification_token)
        user.verify_email()
        session['email'] = user.email

        flash("You have successfully verified your email address.", category="green")
        return redirect(url_for('alerts.index'))
    except errors.UserError as e:
        flash(e.message, 'red')
        return redirect(url_for('users.login_user'))
