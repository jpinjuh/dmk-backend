from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class DistrictQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(District.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist_by_name(self, name):
         try:
             return self.filter(
                 District.status == District.STATUSES['active'],
                 District.name == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_name_is_taken(self, _id, name):
         try:
             return self.filter(
                 District.id != _id,
                 District.status == District.STATUSES['active'],
                 District.username == name).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     @staticmethod
     def query_details():
         from . import City
         return db.session.query(District, City).join(
             City,
             District.city_id == City.id,
             isouter=False)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(District.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def autocomplete_by_name(self, search):
         try:
             from . import City
             return self.query_details().filter(
                 City.status == City.STATUSES['active'],
                 District.status == District.STATUSES['active'],
                 District.name.ilike('%'+search+'%')
             ).all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import City
             return self.query_details().filter(
                 City.status == City.STATUSES['active'],
                 District.status == District.STATUSES['active'],
                 filter_data
             ).order_by(District.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class District(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'districts'

    query_class = DistrictQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    city_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('cities.id'),
                                 nullable=True)
    name = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
