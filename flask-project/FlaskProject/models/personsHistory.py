from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class PersonsHistoryQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(PersonsHistory.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None


    @staticmethod
    def query_details():
        from . import Person, District, User
        return db.session.query(PersonsHistory, Person, District, User) \
            .join(Person, PersonsHistory.mother_id == Person.id, isouter=False) \
            .join(Person, PersonsHistory.father_id == Person.id, isouter=False) \
            .join(District, PersonsHistory.district == District.id, isouter=False) \
            .join(Person, PersonsHistory.person_id == Person.id, isouter=False) \
            .join(User, PersonsHistory.user_created == User.id, isouter=False)

    def get_one_details(self, _id):
        try:
            return self.query_details().filter(PersonsHistory.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def get_all(self):
        try:
            from . import Person, District, User
            return self.query_details().all()
        except Exception as e:
            db.session.rollback()
            return []

    def get_all_by_filter(self, filter_data):
        try:
            from . import Person, District
            return self.query_details().filter(
                # Person.status == Person.STATUSES['active'],
                # District.status == District.STATUSES['active'],
                filter_data
            ).order_by(PersonsHistory.created_at.desc())
        except Exception as e:
            db.session.rollback()
            return []


class PersonsHistory(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'persons_history'

    query_class = PersonsHistoryQuery

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
    birth_place = db.Column(UUID(as_uuid=True),
                            db.ForeignKey('cities.id'),
                            nullable=True)
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
    person = db.Column(UUID(as_uuid=True),
                          db.ForeignKey('persons.id'),
                          nullable=True)
    user_created = db.Column(UUID(as_uuid=True),
                             db.ForeignKey('users.id'),
                             nullable=False)
