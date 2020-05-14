from sqlalchemy import and_

from ... import Archdiocese, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class ArchdioceseController(BaseController):

    def __init__(self, archdiocese=Archdiocese()):
        self.archdiocese = archdiocese

    def create(self):
        """
        Method used for creating archdioceses
        :return: Status object or raise FlaskProjectLogException
        """

        if Archdiocese.query.check_if_already_exist_by_name(
                self.archdiocese.name):
            raise FlaskProjectLogException(
                Status.status_archdiocese_already_exist())

        self.archdiocese.add()
        self.archdiocese.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating archdioceses
        :return: Status object or raise FlaskProjectLogException
        """

        archdiocese = Archdiocese.query.get_one(self.archdiocese.id)

        if archdiocese is None:
            raise FlaskProjectLogException(
                Status.status_archdiocese_not_exist())

        if Archdiocese.query.check_if_name_is_taken(
                archdiocese.id, self.archdiocese.name):
            raise FlaskProjectLogException(
                Status.status_archdiocese_already_exist())

        archdiocese.name = self.archdiocese.name
        archdiocese.update()
        archdiocese.commit_or_rollback()

        self.archdiocese = archdiocese

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting archdioceses status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        archdiocese = Archdiocese.query.get_one(self.archdiocese.id)

        if archdiocese is None:
            raise FlaskProjectLogException(
                Status.status_archdiocese_not_exist())

        archdiocese.status = Archdiocese.STATUSES['inactive']

        archdiocese.update()
        archdiocese.commit_or_rollback()

        self.archdiocese = archdiocese

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting archdioceses status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        archdiocese = Archdiocese.query.get_one(self.archdiocese.id)

        if archdiocese is None:
            raise FlaskProjectLogException(
                Status.status_archdiocese_not_exist())

        if Archdiocese.query.check_if_name_is_taken(
                archdiocese.id, self.archdiocese.name):
            raise FlaskProjectLogException(
                Status.status_archdiocese_already_exist())

        archdiocese.status = Archdiocese.STATUSES['active']

        archdiocese.update()
        archdiocese.commit_or_rollback()

        self.archdiocese = archdiocese

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a archdiocese by identifier
        :param identifier: Extras Archdiocese identifier
        :return: ArchdioceseController object
        """

        return cls(archdiocese=Archdiocese.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get a a archdiocese by identifier
        :param identifier: Archdiocese identifier
        :return: Dict object
        """
        archdiocese = Archdiocese.query.get_one(identifier)

        if archdiocese is not None:
            return obj_to_dict(archdiocese)

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching archdioceses with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            archdiocese = Archdiocese.query.autocomplete_by_name(search)
            for i in archdiocese:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def list_search(search):
        """
        Method for searching archdioceses
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            archdiocese = Archdiocese.query.autocomplete_by_name(search)
            for i in archdiocese:
                list_data.append(obj_to_dict(i))

        else:
            archdiocese = Archdiocese.query.get_all()
            for i in archdiocese:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all archdioceses by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
            #State.status == State.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, Archdiocese.name.ilike('%'+name+'%'))

        data = Archdiocese.query.filter(
            filter_main).order_by(Archdiocese.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)
