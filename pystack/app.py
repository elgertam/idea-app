"""The Flask app, with initialization and view functions."""

import logging

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from pystack import config, filters
from pystack.forms import LoginForm
from pystack.models import Base, User


app = Flask(__name__)
app.config.from_object(config)


# Use Flask-SQLAlchemy for its engine and session configuration. Load the
# extension, giving it the app object, and override its default Model class
# with the pure SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base


# Use Flask-Login to track the current user in Flask's session.
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to see your appointments.'


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return db.session.query(User).get(user_id)


# Load custom Jinja filters from the `filters` module.
filters.init_app(app)


# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) # Log to stderr.
    app.logger.setLevel(logging.INFO)


@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/secure/', methods=['GET'])
@login_required
def secure():
    return render_template('index.html', user=current_user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('appointment_list'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.strip()
        user, authenticated = \
            User.authenticate(db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('secure'))
        else:
            error = 'Incorrect username or password. Try again.'
    return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))
