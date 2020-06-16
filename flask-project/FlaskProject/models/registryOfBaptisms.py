from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class RegistryOfBaptismsQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(RegistryOfBaptisms.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist_by_identity_number(self, identity_number):
         try:
             return self.filter(
                 RegistryOfBaptisms.identity_number == identity_number).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     def check_if_identity_number_is_taken(self, _id, identity_number):
         try:
             return self.filter(
                 RegistryOfBaptisms.id != _id,
                 RegistryOfBaptisms.identity_number == identity_number).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     @staticmethod
     def query_details():
         from . import Person, City, ListItem, Note, District, Archdiocese, Document, User
         best_man = aliased(Person)
         mother = aliased(Person)
         father = aliased(Person)
         parents_canonically_married = aliased(ListItem)
         return db.session.query(RegistryOfBaptisms, Person, best_man, mother, father, City, ListItem, Note, District, Archdiocese, Document, parents_canonically_married, User)\
             .join(
             Person,
             RegistryOfBaptisms.person_id == Person.id,
             isouter=True) \
             .join(best_man, RegistryOfBaptisms.best_man == best_man.id, isouter=True) \
             .join(mother, Person.mother_id == mother.id, isouter=True) \
             .join(father, Person.father_id == father.id, isouter=True) \
             .join(City, RegistryOfBaptisms.birth_place == City.id, isouter=False)\
             .join(ListItem, RegistryOfBaptisms.child == ListItem.id, isouter=False) \
             .join(parents_canonically_married, RegistryOfBaptisms.parents_canonically_married == parents_canonically_married.id, isouter=False) \
             .join(District, Person.district == District.id, isouter=True) \
             .join(Archdiocese, District.archdiocese_id == Archdiocese.id, isouter=True) \
             .join(Document, RegistryOfBaptisms.id == Document.id, isouter=True) \
             .join(User, Document.act_performed == User.id, isouter=True) \
             .join(Note, Note.id == RegistryOfBaptisms.id, isouter=True)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(RegistryOfBaptisms.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def get_all(self):
         try:
             from . import Person, City
             return self.query_details().all()
         except Exception as e:
             db.session.rollback()
             return []

     def get_all_by_filter(self, filter_data):
         try:
             from . import Person, City
             return self.query_details().filter(
                 #Person.status == Person.STATUSES['active'],
                 #City.status == City.STATUSES['active'],
                 filter_data
             ).order_by(RegistryOfBaptisms.created_at.desc())
         except Exception as e:
             db.session.rollback()
             return []


class RegistryOfBaptisms(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'registry_of_baptisms'

    query_class = RegistryOfBaptismsQuery

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
    best_man = db.Column(UUID(as_uuid=True),
                              db.ForeignKey('persons.id'),
                                nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    birth_place = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('cities.id'),
                                 nullable=True)
    identity_number = db.Column(db.String(20), nullable=False)
    child = db.Column(UUID(as_uuid=True),
                      db.ForeignKey("list_items.id"),
                      nullable=False)
    parents_canonically_married = db.Column(UUID(as_uuid=True),
                      db.ForeignKey("list_items.id"),
                      nullable=False)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))



