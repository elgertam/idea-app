"""The Flask app, with initialization and view functions."""
from __future__ import absolute_import

import logging

from flask import Flask
from flask import redirect, render_template, request, url_for
from flask.ext.login import LoginManager, current_user, login_user, login_required, logout_user
from flask.ext.mail import Mail, Message
from flask.ext.sqlalchemy import SQLAlchemy

from . import config, filters
from .forms import LoginForm, IdeaForm, RegisterForm, RequestPasswordReset, PasswordReset
from .models import Base, User, Idea, uuid4

app = Flask(__name__)
app.config.from_object(config)

# Use Flask-SQLAlchemy for its engine and session configuration. Load the
# extension, giving it the app object, and override its default Model class
# with the pure SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

# Use Flask-Login to track the current user in Flask's session.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to add ideas.'

# Initialize Flask-Mail for sending emails
mail = Mail(app)
mail.init_app(app)


def merge_dicts(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return db.session.query(User).get(user_id)

# Load custom Jinja2 filters from the `filters` module.
filters.init_app(app)

# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler())  # Log to stderr.
    app.logger.setLevel(logging.INFO)


@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html', error=error), 404


def save(entity):
    db.session.add(entity)
    db.session.commit()


@app.route('/')
def index():
    user = None
    owned_ideas = 0
    joined_ideas = 0
    if current_user.is_authenticated():
        user = current_user
        owned_ideas = db.session.query(Idea).filter(Idea.owner == user).count()
        joined_ideas = db.session.query(Idea).filter(Idea._members.contains(user)).count()
    return render_template('index.html', user=user, owned_ideas=owned_ideas, joined_ideas=joined_ideas)


@app.route('/secure/', methods=['GET'])
@login_required
def secure():
    return render_template('index.html', user=current_user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.email.data.lower().strip()
        password = form.password.data.strip()
        user, authenticated = User.authenticate(db.session.query, email, password)

        if authenticated:
            login_user(user)
            return redirect(url_for('index'))

        error = 'Incorrect username or password. Try again.'
    return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account_created/')
def account_created():
    return render_template('user/account_created.html')


def user_from_email(email):
    return db.session.query(User).filter(User.email == email.strip().lower()).first()


def user_exists(email):
    return user_from_email(email) is not None


def user_from_register_form(form):
    user = User(
        name=form.first_name.data.strip() + ' ' + form.last_name.data.strip(),
        email=form.email.data.strip().lower(),
        password=form.password.data.strip(),
        active=False,
    )
    return user


def prepare_register_email_message(user):
    subject = 'Idea App - Your Account'
    confirm_url = '{}{}'.format(app.config.get('BASE_URL'), url_for('verify', confirm=user.confirm))
    message = "Your account has been created! Visit {url} to activate your account.".format(url=confirm_url)
    html_message = '<p>{}</p>'.format(message)

    email_message = Message(subject, body=message, html=html_message, recipients=[user.email])

    return email_message


def change_and_notify(user, message_factory=prepare_register_email_message):
    save(user)
    email_message = message_factory(user)
    mail.send(email_message)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        if not user_exists(form.email.data):
            user = user_from_register_form(form)
            change_and_notify(user)
            return redirect(url_for('account_created'))
        error = 'Email ' + form.email.data.lower().strip() + ' already exists!'
    return render_template('user/register.html', form=form, error=error)


def user_from_confirm(confirm):
    return db.session.query(User).filter(User.confirm == confirm).first()


@app.route('/verify/<confirm>/')
def verify(confirm):
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    user = user_from_confirm(confirm)

    if user is not None:
        user.active = True
        save(user)
        return redirect(url_for('login'))

    return render_template('user/verify.html')


@app.route('/request_reset_received/')
def request_reset_received():
    return render_template('user/password_reset_request_received.html')


@app.route('/reset/<confirm>/', methods=['GET', 'POST'])
def reset(confirm):
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = PasswordReset(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        user = user_from_confirm(confirm)
        if user is not None:
            user.active = True
            user.password = form.password.data.strip()
            save(user)
            return redirect(url_for('login'))
        error = 'We had some trouble finding your account. Please check the verification URL you were sent and try again.'

    return render_template('user/password_reset.html', form=form, error=error)


@app.route('/reset/', methods=['GET', 'POST'])
def reset_password():
    if not current_user.is_authenticated():
        return redirect(url_for('request_reset'))

    form = PasswordReset(request.form)

    if request.method == 'POST' and form.validate():
        user = current_user
        user.active = True
        user.password = form.password.data.strip()
        save(user)
        return redirect(url_for('index'))

    return render_template('user/password_reset.html', form=form, error=None)


def prepare_reset_password_email_message(user):
    subject = 'Idea App - Password Reset'
    reset_url = '{}{}'.format(app.config.get('BASE_URL'), url_for('reset', confirm=user.confirm))
    message = 'Your password reset request has been received. Visit {url} to reset your password.'.format(url=reset_url)
    html_message = '<p>{}</p>'.format(message)

    email_message = Message(
        subject,
        body=message,
        html=html_message,
        recipients=[user.email],
    )

    return email_message


@app.route('/request_reset/', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RequestPasswordReset(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        user = user_from_email(form.email.data)
        if user is not None:
            user.confirm = uuid4().get_hex()
            user.active = False
            change_and_notify(user, message_factory=prepare_reset_password_email_message)
            return redirect(url_for('request_reset_received'))
        error = 'We had some trouble finding your account. Please check the verification URL you were sent and try again.'
    return render_template('user/password_reset_request.html', form=form, error=error)


@app.route('/ideas/', methods=['GET', 'POST'])
def ideas():
    all_ideas = db.session.query(Idea).all()
    return render_template('idea/idea_list.html', idea_list=all_ideas)


@app.route('/ideas/new/', methods=['GET', 'POST'])
@login_required
def capture_idea():
    form = IdeaForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        target_idea = Idea(owner=current_user)
        form.populate_obj(target_idea)
        save(target_idea)
        return redirect(url_for('ideas'))
    return render_template('idea/capture_idea.html', form=form, error=error)


@app.route('/ideas/edit/<id_>/', methods=['GET', 'POST'])
@login_required
def edit_idea(id_):
    target_idea = db.session.query(Idea).get(id_)

    if target_idea.owner != current_user:
        return redirect(url_for('ideas'))

    if request.method == 'POST':
        form = IdeaForm(request.form)
        if form.validate():
            form.populate_obj(target_idea)
            save(target_idea)
            return redirect(url_for('ideas'))

    form = IdeaForm(obj=target_idea)
    return render_template('idea/capture_idea.html', form=form, error=None)


@app.route('/ideas/details/<id_>/', methods=['GET'])
@login_required
def idea_details(id_):
    target_idea = db.session.query(Idea).get(id_)
    return render_template('idea/idea_details.html', idea=target_idea, user=current_user)


@app.route('/ideas/join/<id_>/', methods=['GET', 'POST'])
@login_required
def join_idea(id_):
    target_idea = db.session.query(Idea).get(id_)

    if request.method == 'POST':
        joined_idea = target_idea.join(current_user)
        save(joined_idea)
        return redirect(url_for('idea_details', id_=id_))

    return render_template('idea/join_idea.html', idea=target_idea, error=None)


@app.route('/ideas/fork/<id_>/', methods=['GET', 'POST'])
@login_required
def fork_idea(id_):
    target_idea = db.session.query(Idea).get(id_)

    if request.method == 'POST':
        forked_idea = target_idea.fork(current_user)
        save(forked_idea)
        return redirect(url_for('idea_details', id_=forked_idea.id))

    return render_template('idea/fork_idea.html', idea=target_idea, error=None)


@app.route('/ideas/leave/<id_>/', methods=['GET', 'POST'])
@login_required
def leave_idea(id_):
    target_idea = db.session.query(Idea).get(id_)

    if request.method == 'POST':
        left_idea = target_idea.leave(current_user)
        save(left_idea)
        return redirect(url_for('idea_details', id_=id_))

    return render_template('idea/leave_idea.html', idea=target_idea, error=None)
