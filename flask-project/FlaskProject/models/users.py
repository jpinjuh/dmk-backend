from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(User.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist_by_name(self, name):
         try:
             return self.filter(
                 User.status == User.STATUSES['active'],
                 User.username == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_already_exist_by_email(self, email):
         try:
             return self.filter(
                 User.status == User.STATUSES['active'],
                 User.email == email).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_name_is_taken(self, _id, name):
         try:
             return self.filter(
                 User.id != _id,
                 User.status == User.STATUSES['active'],
                 User.username == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False


     def check_if_email_is_taken(self, _id, email):
         try:
             return self.filter(
                 User.id != _id,
                 User.status == User.STATUSES['active'],
                 User.email == email).first() is not None
         except Exception as e:
             db.session.rollback()
             return False


     @staticmethod
     def query_details():
         from . import Role, District
         return db.session.query(User, Role, District)\
             .join(
             Role,
             User.roles_id == Role.id,
             isouter=False)\
             .join(District, User.districts_id == District.id, isouter=False)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(User.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def autocomplete_by_name(self, search):
         try:
             from . import Role, District
             return self.query_details().filter(
                 Role.status == Role.STATUSES['active'],
                 District.status == District.STATUSES['active'],
                 User.status == User.STATUSES['active'],
                 User.first_name.ilike('%'+search+'%'),
                 User.last_name.ilike('%'+search+'%'),
                 User.username.ilike('%' + search + '%')
             ).all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import Role, District
             return self.query_details().filter(
                 #Role.status == Role.STATUSES['active'],
                 #District.status == District.STATUSES['active'],
                 #User.status == User.STATUSES['active'],
                 filter_data
             ).order_by(User.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class User(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'users'

    query_class = UserQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    roles_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('roles.id'),
                                 nullable=True)
    districts_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('districts.id'),
                                 nullable=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password) or user.status != User.STATUSES['active']:
            return None

        return user
