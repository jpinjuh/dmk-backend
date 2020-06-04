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
    place_of_burial = db.Column(UUID(as_uuid=False),
                                 db.ForeignKey('list_items.id'),
                                 nullable=True)
    date_of_burial = db.Column(db.Date, nullable=False)
    act_performed = db.Column(UUID(as_uuid=True),
                      db.ForeignKey("users.id"),
                      nullable=False)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))



