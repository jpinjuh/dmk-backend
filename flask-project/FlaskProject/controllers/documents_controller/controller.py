from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ..listItems_controller.controller import ListItemController
from ..users_controller.controller import UserController
from ..districts_controller.controller import DistrictController
from ... import Document, ListItem, Person, User, District, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class DocumentController(BaseController):
    def __init__(self, document=Document()):
        self.document = document

    def create(self):
        """
         Method used for creating document
        :return: Status object or raise FlaskProjectLogException
        """
        if self.document.document_type is not None:
            document_type = ListItemController.get_one(
                self.document.document_type)

            if document_type.list_item is None:
                raise FlaskProjectLogException(
                    Status.status_list_item_not_exist())

        if self.document.person_id is not None:
            person = PersonController.get_one(
                self.document.person_id)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.document.person2_id is not None:
            person2 = PersonController.get_one(
                self.document.person2_id)

            if person2.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.document.district is not None:
            district = DistrictController.get_one(
                self.document.district)

            if district.district is None:
                raise FlaskProjectLogException(
                    Status.status_district_not_exist())

        if self.document.user_created is not None:
            user_created = UserController.get_one(
                self.document.user_created)

            if user_created.user is None:
                raise FlaskProjectLogException(
                    Status.status_user_not_exist())

        self.document.add()
        self.document.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(document=Document.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an document by identifier
       :param identifier: Document identifier
       :return: Dict object
       """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_search(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all documents by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
        # Document.status == Document.STATUSES['active'])

        document_type = kwargs.get('document_type', None)
        person_id = kwargs.get('person_id', None)
        person2_id = kwargs.get('person2_id', None)
        act_date = kwargs.get('act_date', None)
        act_performed = kwargs.get('act_performed', None)
        document_number = kwargs.get('document_number', None)
        district = kwargs.get('district', None)
        volume = kwargs.get('volume', None)
        year = kwargs.get('year', None)
        page = kwargs.get('page', None)
        number = kwargs.get('number', None)

        if document_type:
            filter_main = and_(
                filter_main, Document.document_type.ilike('%' + document_type + '%'))

        if person_id:
            filter_main = and_(
                filter_main, Document.person_id.ilike('%' + person_id + '%'))

        if person2_id:
            filter_main = and_(
                filter_main, Document.person2_id.ilike('%' + person2_id + '%'))

        if act_date:
            filter_main = and_(
                filter_main, Document.act_date.ilike('%' + act_date + '%'))

        if act_performed:
            filter_main = and_(
                filter_main, Document.act_performed.ilike('%' + act_performed + '%'))

        if document_number:
            filter_main = and_(
                filter_main, Document.document_number.ilike('%' + document_number + '%'))

        if district:
            filter_main = and_(
                filter_main, District.id == district)

        if volume:
            filter_main = and_(
                filter_main, Document.volume.ilike('%' + volume + '%'))

        if year:
            filter_main = and_(
                filter_main, Document.year.ilike('%' + year + '%'))

        if page:
            filter_main = and_(
                filter_main, Document.page.ilike('%' + page + '%'))

        if number:
            filter_main = and_(
                filter_main, Document.number.ilike('%' + number + '%'))

        data = Document.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(DocumentController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.Document)
            person = Person.query.filter_by(id=row_data.Document.person_id).first()
            person2 = Person.query.filter_by(id=row_data.Document.person2_id).first()
            act_performed = User.query.filter_by(id=row_data.Document.act_performed).first()
            return_dict['document_type'] = obj_to_dict(row_data.ListItem)
            return_dict['person'] = obj_to_dict(person)
            return_dict['person2'] = obj_to_dict(person2)
            return_dict['act_performed'] = obj_to_dict(act_performed)
            return_dict['district'] = obj_to_dict(row_data.District)
            return return_dict
        return None


