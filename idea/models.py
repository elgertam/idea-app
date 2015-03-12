"""Domain models for a user, using pure SQLAlchemy."""
from __future__ import absolute_import, print_function

import attr

from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import synonym, relationship, class_mapper
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.security import check_password_hash, generate_password_hash

from uuid import uuid4

naming_conventions = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_conventions)
Base = declarative_base(metadata=metadata)

members = Table('members', Base.metadata,
                Column('idea', Integer, ForeignKey('idea.id'), primary_key=True),
                Column('user', Integer, ForeignKey('user.id'), primary_key=True),
                )


class Idea(Base):
    """Information for a specific Idea"""
    __tablename__ = 'idea'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    _forked_from_id = Column('forked_from_id', Integer, ForeignKey('idea.id'))
    _owner_id = Column('owner_id', Integer, ForeignKey('user.id'))

    title = Column(String(200))
    problem = Column(String, nullable=False)
    solution = Column(String, nullable=False)
    archive = Column(Boolean, default=False, nullable=False)

    owner = relationship('User')
    _members = relationship('User', secondary=members)
    forked_from = relationship('Idea', backref='forks', remote_side=[id])

    def fork(self, owner):
        if owner == self.owner:
            raise RuntimeError('An owner cannot fork his or her own idea')
        new_idea = Idea(title=self.title,
                        problem=self.problem,
                        solution=self.solution,
                        forked_from=self,
                        owner=owner)
        return new_idea

    def join(self, user):
        if self.owner == user:
            raise RuntimeError('An owner cannot become a member of his or her own idea')
        if user in self.members:
            raise RuntimeError('')


class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name = Column(String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    confirm = Column(String(32), unique=True, nullable=False, default=(lambda: uuid4().get_hex()))

    _password = Column('password', String(100), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    # Hooks for Flask-Login.
    #
    # As methods, these are only valid for User instances, so the
    # authentication will have already happened in the view functions.
    #
    # If you prefer, you can use Flask-Login's UserMixin to get these methods.

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.active

    # noinspection PyMethodMayBeStatic
    def is_anonymous(self):
        return False

    # noinspection PyMethodMayBeStatic
    def is_authenticated(self):
        return True

Idea = attr.s(these={prop.key: attr.ib() for prop in class_mapper(Idea).iterate_properties}, init=False)(Idea)
User = attr.s(these={prop.key: attr.ib() for prop in class_mapper(User).iterate_properties}, init=False)(User)
