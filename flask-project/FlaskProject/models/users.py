from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


# class TestFilmQuery(BaseQuery):

#     def get_one(self, _id):
#         try:
#             return self.filter(TestFilm.id == _id).first()
#         except Exception as e:
#             db.session.rollback()
#             return None

#     @staticmethod
#     def query_details():
#         from . import TestCategory
#         return db.session.query(TestFilm, TestCategory).join(
#             TestCategory,
#             TestFilm.test_category_id == TestCategory.id,
#             isouter=False)

#     def get_one_details(self, _id):
#         try:
#             return self.query_details().filter(TestFilm.id == _id).first()
#         except Exception as e:
#             db.session.rollback()
#             return None

#     def autocomplete_by_name(self, search):
#         try:
#             from . import TestCategory
#             return self.query_details().filter(
#                 TestCategory.status == TestCategory.STATUSES['active'],
#                 TestFilm.status == TestFilm.STATUSES['active'],
#                 TestFilm.name.ilike('%'+search+'%')
#             ).all()
#         except Exception as e:
#             db.session.rollback()
#             return []

#     def get_all_by_filter(self, filter_data):
#         try:
#             from . import TestCategory
#             return self.query_details().filter(
#                 TestCategory.status == TestCategory.STATUSES['active'],
#                 TestFilm.status == TestFilm.STATUSES['active'],
#                 filter_data
#             ).order_by(TestFilm.created_at.desc())
#         except Exception as e:
#             db.session.rollback()
#             return []


class User(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'users'

    #query_class = TestFilmQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    roles_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('roles.id'),
                                 nullable=True)
    districts_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('districts.id'),
                                 nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
