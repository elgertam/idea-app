"""Application configuration.

When using app.config.from_object(obj), Flask will look for all UPPERCASE
attributes on that object and load their values into the app config. Python
modules are objects, so you can use a .py file as your configuration.
"""

import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://elgertam@localhost/idea'
SECRET_KEY = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'  # Create your own.
SESSION_PROTECTION = 'strong'

BASE_URL = 'http://localhost:5000'

MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'noreply@konkourse.com'
