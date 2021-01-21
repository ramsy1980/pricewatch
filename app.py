import os
from flask import Flask, render_template, request
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from views.emails import email_blueprint

APP_SECRET = os.environ.get('APP_SECRET')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

if APP_SECRET is None:
    raise RuntimeError("Failed to load APP_SECRET")
if ADMIN_EMAIL is None:
    raise RuntimeError("Failed to load ADMIN_EMAIL")

app = Flask(__name__)

app.secret_key = APP_SECRET

app.config.update(
    ADMIN_EMAIL=ADMIN_EMAIL,
)


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(email_blueprint, url_prefix="/emails")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
