"""Application configuration.

When using app.config.from_object(obj), Flask will look for all UPPERCASE
attributes on that object and load their values into the app config. Python
modules are objects, so you can use a .py file as your configuration.
"""

import os

# Get the current working directory to place idea-app.db during development.
# In production, use absolute paths or a database management system.
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/idea-app.db'.format(PWD)
SECRET_KEY = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf' # Create your own.
SESSION_PROTECTION = 'strong'

MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = None
MAIL_PASSWORD = None
DEFAULT_MAIL_SENDER = None