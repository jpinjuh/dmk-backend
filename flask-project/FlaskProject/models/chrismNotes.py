from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db
from sqlalchemy import or_
from sqlalchemy.orm import relationship, foreign, aliased


class ChrismNoteQuery(BaseQuery):

     def get_one(self, _id):
         try:
             return self.filter(ChrismNote.id == _id).first()
         except Exception as e:
             db.session.rollback()
             return None


class ChrismNote(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'chrism_notes'

    query_class = ChrismNoteQuery

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
                                nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))






