from flask import Blueprint, flash, redirect, url_for
from models.user import requires_login

payment_blueprint = Blueprint('payments', __name__)


@payment_blueprint.route('/success')
@requires_login
def payment_successful():
    flash("Your payment was successful!", "green")
    return redirect(url_for('credits.index'))


@payment_blueprint.route('/cancelled')
@requires_login
def payment_cancelled():
    flash("Your payment was cancelled!", "yellow")
    return redirect(url_for('credits.index'))
