"""Application configuration.

When using app.config.from_object(obj), Flask will look for all UPPERCASE
attributes on that object and load their values into the app config. Python
modules are objects, so you can use a .py file as your configuration.
"""

import os

DATABASE_USER = os.getenv('DATABASE_USER', 'elgertam')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'idea')
default_db_uri = 'postgresql://{user}@{host}/{name}'.format(user=DATABASE_USER, host=DATABASE_HOST, name=DATABASE_NAME)

DEBUG = os.getenv('DEBUG', 'true') == 'true'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_db_uri)
SECRET_KEY = os.getenv('SECRET_KEY', 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf')  # Create your own.
SESSION_PROTECTION = 'strong'

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
MAIL_PORT = os.getenv('MAIL_PORT', 1025)
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'false').lower() == 'true'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
MAIL_DEBUG = os.getenv('MAIL_DEBUG', DEBUG) is True
MAIL_USERNAME = os.getenv('MAIL_USERNAME', None)
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', None)
MAIL_DEFAULT_SENDER = 'noreply@elgert.org'
