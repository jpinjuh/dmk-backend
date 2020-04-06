import datetime

from ..general import FlaskProjectLogException
from ..db import db
from ..general import Status


class ModelsMixin:

    @staticmethod
    def commit_or_rollback():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise FlaskProjectLogException(Status(-101, str(e)))

    def add(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at
        db.session.add(self)

    def update(self):
        self.updated_at = datetime.datetime.now()
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

