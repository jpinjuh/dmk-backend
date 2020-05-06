from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class StateQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(State.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def check_if_already_exist_by_name(self, name):
        try:
            return self.filter(
                State.status == State.STATUSES['active'],
                State.name == name).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    def check_if_name_is_taken(self, _id, name):
        try:
            return self.filter(
                State.id != _id,
                State.status == State.STATUSES['active'],
                State.name == name).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    def autocomplete_by_name(self, search):
        try:
            return self.filter(
                State.status == State.STATUSES['active'],
                State.name.ilike('%'+search+'%')).all()
        except Exception as e:
            db.session.rollback()
            return []

    def search_by_name(self, search):
        try:
            return self.filter(
                State.status == State.STATUSES['active'],
                State.name.ilike('%' + search + '%')).all()
        except Exception as e:
            db.session.rollback()
            return []

    def get_all(self):
        try:
            return self.order_by(State.created_at.desc()).all()
        except Exception as e:
            db.session.rollback()
            return []


class State(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'states'

    query_class = StateQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
