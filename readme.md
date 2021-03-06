Idea App
========

## Pre-Setup ##

Before you can run this project, you will need to set up a database
(in the code below, we have assumed the name 'idea'). PostgreSQL is
recommended, but MySQL or even SQL Server can be used. (SQLite has acted
quite finicky with migrations, so it is not recommended.) Once you have
set up your database, please edit the connection uri in config.py:

    SQLALCHEMY_DATABASE_URI = 'postgresql://<user>:<pass>@<host>/idea'

For SQL Server use:

    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://<user>:<pass>@<host>/idea'

Please consult the [SQLAlchemy Documentation](http://docs.sqlalchemy.org/en/rel_1_0/)
for further information.

## Setup ##

To set up this project, create a virtualenv with Python 2.7 or Python
3.3+, activate that virtualenv, then set up your application with these
commands:

    pip install -r <env>.requirements.txt  # <env> is win for Windows and osx for Mac OS X
    python manage.py db upgrade

## Commands ##

Create a user in the Python shell:

    python manage.py shell

By executing this Python code in the interactive interpreter:

    from idea.app import db, User
    user = User(email='you@example.com', password='secret')
    db.session.add(user)
    db.session.commit()

## Run ##

Start the development server with:

    python manage.py runserver

Start the email server with:

    python manage.py email

Based on [Ron DuPlain's Sched](https://github.com/rduplain/sched)
