"""Forms to render HTML input & validate request data."""

from wtforms import Form, PasswordField, TextAreaField, StringField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.validators import Length, required, Required, EqualTo, Email


class LoginForm(Form):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])



class IdeaForm(Form):
    title = StringField('Idea Title', [DataRequired()])
    problem = TextAreaField('Problem', [DataRequired()])
    solution = TextAreaField('Solution', [DataRequired()])


class RegisterForm(Form):
    """Render HTML input for sign-up form."""
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    last_name = StringField('Last Name', [DataRequired()])
    first_name = StringField('First Name', [DataRequired()])


class RequestPasswordReset(Form):
    """Render HTML input for password reset request form"""
    email = StringField('Email', [DataRequired(), Email()])


class PasswordReset(Form):
    """Render HTML input for password reset form"""
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
