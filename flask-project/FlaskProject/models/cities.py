from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_

class CityQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(City.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist_by_name(self, name):
         try:
             return self.filter(
                 City.status == City.STATUSES['active'],
                 City.name == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_name_is_taken(self, _id, name):
         try:
             return self.filter(
                 City.id != _id,
                 #City.status == City.STATUSES['active'],
                 City.name == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     @staticmethod
     def query_details():
         from . import State
         return db.session.query(City, State).join(
             State,
             City.state_id == State.id,
             isouter=False)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(City.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def autocomplete_by_name(self, search):
         try:
             from . import State
             return self.query_details().filter(
                 #State.status == State.STATUSES['active'],
                 #City.status == City.STATUSES['active'],
                 or_(City.name.ilike('%'+search+'%'),
                     State.name.ilike('%'+search+'%'))
             ).all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all(self):
         try:
             from . import State
             return self.query_details().order_by(City.created_at.desc()).all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import State
             return self.query_details().filter(
                 #State.status == State.STATUSES['active'],
                 #City.status == City.STATUSES['active'],
                 filter_data
             ).order_by(City.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class City(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'cities'

    query_class = CityQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    state_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('states.id'),
                                 nullable=True)
    name = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
