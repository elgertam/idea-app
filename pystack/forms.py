"""Forms to render HTML input & validate request data."""

from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required, Required, EqualTo


class LoginForm(Form):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])

class IdeaForm(Form):
    idea_title = TextField('Idea Title', [required()])
    idea_description = TextField('Idea Description')
    idea_author = TextField('IdeaAuthor')
    idea_notes = TextField('IdeaNotes')
    project_members = TextField(u'ProjectMembers')

class SignUpForm(Form):
    """Render HTML input for sign-up form."""

    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Password', [Required(), EqualTo('password')])
