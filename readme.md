=======================================================================
 pystack
=======================================================================

To run this project, create a virtualenv with Python 2.7 or Python
3.3+, activate that virtualenv, then set up your application with these
commands:

    pip install -r stable.txt
    python manage.py create_tables

Create a user in the Python shell:

    python manage.py shell

By executing this Python code in the interactive interpreter:

    from pystack.app import db, User
    user = User(email='you@example.com', password='secret')
    db.session.add(user)
    db.session.commit()

Start the development server with:

    python manage.py runserver

Based on Ron DuPlain's Sched https://github.com/rduplain/sched
