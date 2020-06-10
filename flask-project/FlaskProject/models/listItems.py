from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class ListItemQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(ListItem.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def check_if_value_already_exist_in_list(self, list_id, value):
        try:
            return self.filter(
                #ListItem.status == ListItem.STATUSES['active'],
                ListItem.list_id == list_id, ListItem.value == value).first() is not None
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def query_details():
         from . import List
         return db.session.query(ListItem, List)\
             .join(
             List,
             ListItem.list_id == List.id,
             isouter=False)

    def get_list_items(self, list_id):
        try:
            from . import List
            return self.query_details().filter(
                # List.status == List.STATUSES['active'],
                # ListItem.status == ListItem.STATUSES['active'],
                ListItem.list_id == list_id
            ).order_by(ListItem.created_at.desc())
        except Exception as e:
            db.session.rollback()
            return []

    def get_all_by_filter(self, filter_data):
        try:
            from . import List
            return self.query_details().filter(
                # List.status == List.STATUSES['active'],
                # ListItem.status == ListItem.STATUSES['active'],
                filter_data
            ).order_by(ListItem.created_at.desc())
        except Exception as e:
            db.session.rollback()
            return []

class ListItem(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'list_items'

    query_class = ListItemQuery

    STATUSES = {
        'active': 1,
        'inactive': 0
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    auxiliary_description = db.Column(UUID(as_uuid=True), nullable=True)
    list_id = db.Column(UUID(as_uuid=True),
                                db.ForeignKey('lists.id'),
                                nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
