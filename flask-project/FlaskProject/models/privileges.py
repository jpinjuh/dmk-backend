from uuid import uuid4
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects.postgresql import UUID

from . import TimestampedModelMixin, ModelsMixin
from ..db import db


class PrivilegeQuery(BaseQuery):

    def get_one(self, _id):
        try:
            return self.filter(Privilege.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    @staticmethod
    def query_details():
        from . import Role, Permission
        return db.session.query(Privilege, Role, Permission) \
            .join(
            Role,
            Privilege.roles_id == Role.id,
            isouter=False) \
            .join(Permission, Privilege.permissions_id == Permission.id, isouter=False)

    def get_one_details(self, _id):
        try:
            return self.query_details().filter(Privilege.id == _id).first()
        except Exception as e:
            db.session.rollback()
            return None

    def autocomplete_by_name(self, search):
        try:
            from . import Role, Permission
            return self.query_details().filter(
                Role.status == Role.STATUSES['active'],
                Permission.status == Permission.STATUSES['active'],
                Privilege.status == Privilege.STATUSES['active'],
            ).all()
        except Exception as e:
            db.session.rollback()
            return []

    def get_all_by_filter(self, filter_data):
        try:
            from . import Role, Permission
            return self.query_details().filter(
                Role.status == Role.STATUSES['active'],
                Permission.status == Permission.STATUSES['active'],
                Privilege.status == Privilege.STATUSES['active'],
                filter_data
            ).order_by(Privilege.created_at.desc())
        except Exception as e:
            db.session.rollback()
            return []


class Privilege(ModelsMixin, TimestampedModelMixin, db.Model):

    __tablename__ = 'privileges'

    query_class = PrivilegeQuery

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
    permissions_id = db.Column(UUID(as_uuid=True),
                                 db.ForeignKey('permissions.id'),
                                 nullable=True)
    status = db.Column(
        db.SmallInteger, nullable=False,
        default=STATUSES['active'], server_default=str(STATUSES['active']))
