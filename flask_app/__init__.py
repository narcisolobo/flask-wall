import datetime
import secrets
import timeago
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = secrets.token_hex()
bcrypt = Bcrypt(app)


@app.template_filter('int')
def intify(val):
    return int(val)


@app.template_filter('str')
def stringify(val):
    return str(val)


@app.template_filter('type')
def check_type(val):
    return type(val)


@app.template_filter('timeago')
def relative_time(val):
    now = datetime.datetime.now()
    return timeago.format(val, now)
