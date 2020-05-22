from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class DocumentQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(Document.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist_by_document_number(self, document_number):
         try:
             return self.filter(
                 Document.document_number == document_number).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_document_number_is_taken(self, _id, document_number):
         try:
             return self.filter(
                 Document.id != _id,
                 Document.document_number == document_number).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     @staticmethod
     def query_details():
         from . import Person, User, District, ListItem
         person1 = aliased(Person)
         person2 = aliased(Person)
         user1 = aliased(User)
         user2 = aliased(User)
         return db.session.query(Document, District, person1, person2, user1, user2, ListItem) \
             .outerjoin(person1, Document.person_id == person1.id) \
             .outerjoin(person2, Document.person2_id == person2.id) \
             .outerjoin(user1, Document.act_performed == user1.id) \
             .outerjoin(user2, Document.user_created == user2.id)\
             .join(District, Document.district == District.id, isouter=False) \
             .join(ListItem, Document.document_type == ListItem.id, isouter=False)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(Document.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def get_all(self):
         try:
             from . import Person, User, District
             return self.query_details().all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import Person, User, District
             return self.query_details().filter(
                 #Person.status == Person.STATUSES['active'],
                 #User.status == User.STATUSES['active'],
                 #District.status == District.STATUSES['active'],
                 filter_data
             ).order_by(Document.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class Document(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'documents'

    query_class = DocumentQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    document_type = db.Column(UUID(as_uuid=True),
                              db.ForeignKey('list_items.id'),
                              nullable=False)
    person_id = db.Column(UUID(as_uuid=True),
                                db.ForeignKey('persons.id'),
                                nullable=False)
    person2_id = db.Column(UUID(as_uuid=True),
                                db.ForeignKey('persons.id'),
                                nullable=True)
    act_date = db.Column(db.Date, nullable=False)
    act_performed = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('users.id'),
                                 nullable=False)
    document_number = db.Column(db.String(30), nullable=False)
    district = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('districts.id'),
                                 nullable=True)
    volume = db.Column(db.String(10), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    page = db.Column(db.Integer, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    user_created = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('users.id'),
                                 nullable=False)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))






