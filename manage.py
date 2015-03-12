#!/usr/bin/env python
from __future__ import print_function

import smtpd

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from idea.app import app, db

# By default, Flask-Script adds the 'runserver' and 'shell' commands to
# interact with the Flask application. Add additional commands using the
# `@manager.command` decorator, where Flask-Script will create help
# documentation using the function's docstring. Try it, and call `python
# manage.py -h` to see the outcome.
manager = Manager(app)


@manager.command
def email():
    """Run test email server using project config"""
    addr = app.config['MAIL_SERVER'], app.config['MAIL_PORT']
    print('Running email server on {}:{}'.format(*addr))
    smtp_server = smtpd.DebuggingServer(addr, None)
    try:
        smtpd.asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
