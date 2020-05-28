from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class CounterQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(Archdiocese.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def check_if_already_exist_by_name(self, name):
        try:
            return self.filter(
                #Archiodese.status == Archdiocese.STATUSES['active'],
                Archdiocese.name == name).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    def check_if_name_is_taken(self, _id, name):
        try:
            return self.filter(
                Archdiocese.id != _id,
                #Archiodese.status == Archiodese.STATUSES['active'],
                Archdiocese.name == name).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    def autocomplete_by_name(self, search):
        try:
            return self.filter(
                Archdiocese.status == Archdiocese.STATUSES['active'],
                Archdiocese.name.ilike('%'+search+'%')).all()
        except Exception as e:
            db.session.rollback()
            return []

    def get_all(self):
        try:
            return self.all()
        except Exception as e:
            db.session.rollback()
            return []


class Counter(ModelsMixin, db.Model):

    __tablename__ = 'counter'

    query_class = CounterQuery

    counters = {
        "document_name": 'ed33ab9d-3bb9-4251-b527-d897981df675'
    }

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    expression = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    restart_on = db.Column(db.String(255), nullable=False)
    start_from = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    restart_time = db.Column(db.DateTime(timezone=False), nullable=True)
    status = db.Column(
        db.Integer, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
