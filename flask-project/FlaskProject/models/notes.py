from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_

class NoteQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(Note.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     @staticmethod
     def query_details():
         from . import Person, City, District
         return db.session.query(Note, Person, City, District).join(
             Person,
             Note.person_id == Person.id,
             isouter=False)\
             .join(City, Note.chrism_place == City.id, isouter=False)\
             .join(District, Note.marriage_district == District.id, isouter=False)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(Note.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def get_all(self):
         try:
             from . import Person
             return self.query_details().all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import Person
             return self.query_details().filter(
                 #Note.status == Note.STATUSES['active'],
                 #Person.status == Person.STATUSES['active'],
                 filter_data
             ).order_by(Note.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class Note(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'notes'

    query_class = NoteQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    person_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('persons.id'),
                                 nullable=False)
    chrism_place = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('cities.id'),
                                 nullable=True)
    chrism_date = db.Column(db.Date, nullable=True)
    marriage_district = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('districts.id'),
                                 nullable=True)
    marriage_date = db.Column(db.Date, nullable=True)
    spouse_name = db.Column(db.String(255), nullable=True)
    other_notes = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
