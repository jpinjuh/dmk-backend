from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID
from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class RegistryOfDeathsQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(RegistryOfDeaths.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

     def check_if_already_exist(self, id):
         try:
             return self.filter(
                 RegistryOfDeaths.person_id == id).first() is not None
         except Exception as e:
             db.session.rollback()
             return False

     @staticmethod
     def query_details():
         from . import Person, City, ListItem, Document, Note, District, Archdiocese, User
         mother = aliased(Person)
         father = aliased(Person)
         return db.session.query(RegistryOfDeaths, Person, mother, father, City, ListItem, Document, Note, District, Archdiocese, User)\
             .join(
             Person,
             RegistryOfDeaths.person_id == Person.id,
             isouter=True) \
             .join(City, RegistryOfDeaths.place_of_death == City.id, isouter=False) \
             .join(ListItem, RegistryOfDeaths.place_of_burial == ListItem.id, isouter=False) \
             .join(mother, Person.mother_id == mother.id, isouter=True) \
             .join(father, Person.father_id == father.id, isouter=True) \
             .join(District, Person.district == District.id, isouter=True) \
             .join(Archdiocese, District.archdiocese_id == Archdiocese.id, isouter=True) \
             .join(Document, RegistryOfDeaths.id == Document.id, isouter=True) \
             .join(User, Document.act_performed == User.id, isouter=True) \
             .join(Note, Note.id == RegistryOfDeaths.id, isouter=True)

     def get_one_details(self, _id):
         try:
             return self.query_details().filter(RegistryOfDeaths.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None

class RegistryOfDeaths(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'registry_of_deaths'

    query_class = RegistryOfDeathsQuery

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
    date_of_death = db.Column(db.Date, nullable=False)
    place_of_death = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('cities.id'),
                                 nullable=True)
    place_of_burial = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('list_items.id'),
                                 nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))



