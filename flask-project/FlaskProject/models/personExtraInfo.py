from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID
from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class PersonExtraInfoQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(PersonExtraInfo.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None


class PersonExtraInfo(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'person_extra_info'

    query_class = PersonExtraInfoQuery

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
    baptism_district = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('districts.id'),
                                 nullable=True)
    baptism_date = db.Column(db.Date, nullable=True)
    parents_canonically_married = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('list_items.id'),
                                 nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))



