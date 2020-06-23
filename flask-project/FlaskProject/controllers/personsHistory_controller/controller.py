from sqlalchemy import and_
from ..persons_controller.controller import PersonController
from ..listItems_controller.controller import ListItemController
from ..users_controller.controller import UserController
from ..districts_controller.controller import DistrictController
from ... import PersonsHistory, District, ListItem, Person, User, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class PersonsHistoryController(BaseController):
    def __init__(self, personsHistory=PersonsHistory()):
        self.personsHistory = personsHistory

    def create(self):
        """
         Method used for creating persons history
        :return: Status object or raise FlaskProjectLogException
        """
        if self.personsHistory.mother_id is not None:
            mother = PersonController.get_one(
                self.personsHistory.mother_id)

            if mother.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.personsHistory.father_id is not None:
            father = PersonController.get_one(
                self.personsHistory.father_id)

            if father.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.personsHistory.district is not None:
            district = DistrictController.get_one(
                self.personsHistory.district)

            if district.district is None:
                raise FlaskProjectLogException(
                    Status.status_district_not_exist())

        if self.personsHistory.religion is not None:
            religion = ListItemController.get_one(
                self.personsHistory.religion)

            if religion.list_item is None:
                raise FlaskProjectLogException(
                    Status.status_list_item_not_exist())

        if self.personsHistory.person is not None:
            person = PersonController.get_one(
                self.personsHistory.person)

            if person.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.personsHistory.user_created is not None:
            user_created = UserController.get_one(
                self.personsHistory.user_created)

            if user_created.user is None:
                raise FlaskProjectLogException(
                    Status.status_user_not_exist())

        self.personsHistory.add()
        self.personsHistory.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(personsHistory=PersonsHistory.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get a persons history by identifier
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
        Method for getting all persons history by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        first_name = kwargs.get('first_name', None)
        last_name = kwargs.get('last_name', None)
        maiden_name = kwargs.get('maiden_name', None)
        birth_date = kwargs.get('birth_date', None)
        identity_number = kwargs.get('identity_number', None)
        father_id = kwargs.get('father_id', None)
        mother_id = kwargs.get('mother_id', None)
        district = kwargs.get('district', None)
        religion = kwargs.get('religion', None)
        person = kwargs.get('person', None)
        user_created = kwargs.get('user_created', None)

        if first_name:
            filter_main = and_(
                filter_main, PersonsHistory.first_name.ilike('%' + first_name + '%'))

        if last_name:
            filter_main = and_(
                filter_main, PersonsHistory.last_name.ilike('%' + last_name + '%'))

        if maiden_name:
            filter_main = and_(
                filter_main, PersonsHistory.maiden_name.ilike('%' + maiden_name + '%'))

        if birth_date:
            filter_main = and_(
                filter_main, PersonsHistory.birth_date.ilike('%' + birth_date + '%'))

        if identity_number:
            filter_main = and_(
                filter_main, PersonsHistory.identity_number.ilike('%' + identity_number + '%'))

        if father_id:
            filter_main = and_(
                filter_main, Person.id == father_id)

        if mother_id:
            filter_main = and_(
                filter_main, Person.id == mother_id)

        if district:
            filter_main = and_(
                filter_main, District.id == district)

        if religion:
            filter_main = and_(
                filter_main, ListItem.id == religion)

        if person:
            filter_main = and_(
                filter_main, Person.id == person)

        if user_created:
            filter_main = and_(
                filter_main, User.id == user_created)

        data = PersonsHistory.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(PersonsHistoryController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.PersonsHistory)
            mother = Person.query.filter_by(id=row_data.PersonsHistory.mother_id).first()
            father = Person.query.filter_by(id=row_data.PersonsHistory.father_id).first()
            person = Person.query.filter_by(id=row_data.PersonsHistory.person).first()
            user_created = User.query.filter_by(id=row_data.PersonsHistory.user_created).first()
            return_dict['mother'] = obj_to_dict(mother)
            return_dict['father'] = obj_to_dict(father)
            return_dict['religion'] = obj_to_dict(row_data.ListItem)
            return_dict['district'] = obj_to_dict(row_data.District)
            return_dict['person'] = obj_to_dict(person)
            return_dict['user_created'] = obj_to_dict(user_created)
            return return_dict
        return None


