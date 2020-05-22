from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy.orm import relationship, foreign, aliased


class PersonQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(Person.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def check_if_already_exist_by_id_number(self, identity_number):
        try:
            return self.filter(
                Person.identity_number == identity_number).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    def check_if_id_number_is_taken(self, _id, identity_number):
        try:
            return self.filter(
                Person.id != _id,
                Person.identity_number == identity_number).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def query_details():
        from . import District, Person, ListItem
        mother = aliased(Person)
        father = aliased(Person)
        return db.session.query(Person, District, mother, father, ListItem) \
            .outerjoin(mother, Person.mother_id == mother.id)\
            .outerjoin(father, Person.father_id == father.id)\
            .join(District, Person.district == District.id, isouter=False)\
            .join(ListItem, Person.religion == ListItem.id, isouter=False)

    def get_one_details(self, _id):
        try:
            return self.query_details().filter(Person.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def get_all(self):
        try:
            from . import District
            return self.query_details().all()
        except Exception as e:
            db.session.rollback()
            return []

    def get_all_by_filter(self, filter_data):
        try:
            from . import District
            return self.query_details().filter(
                # Person.status == Person.STATUSES['active'],
                # District.status == District.STATUSES['active'],
                filter_data
            ).order_by(Person.created_at.desc())
        except Exception as e:
            db.session.rollback()
            return []


class Person(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'persons'

    query_class = PersonQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    maiden_name = db.Column(db.String(50), nullable=True)
    birth_date = db.Column(db.Date, nullable=False)
    identity_number = db.Column(db.String(20), nullable=False)
    father_id = db.Column(UUID(as_uuid=True),
                         db.ForeignKey('persons.id'),
                         nullable=True)
    mother_id = db.Column(UUID(as_uuid=True),
                       db.ForeignKey('persons.id'),
                       nullable=True)
    district = db.Column(UUID(as_uuid=True),
                             db.ForeignKey('districts.id'),
                             nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))

    religion = db.Column(UUID(as_uuid=True),
                      db.ForeignKey("list_items.id"),
                      nullable=False)
    mother = db.relationship("Person", foreign_keys=[mother_id])
    father = db.relationship("Person", foreign_keys=[father_id])
