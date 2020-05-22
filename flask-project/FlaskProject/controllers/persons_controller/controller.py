from sqlalchemy import and_
from ..districts_controller.controller import DistrictController
from ..listItems_controller.controller import ListItemController
from ... import Person, FlaskProjectLogException, District, ListItem
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class PersonController(BaseController):

    def __init__(self, person=Person()):
        self.person = person

    def create(self):
        """
        Method used for creating persons
        :return: Status object or raise FlaskProjectLogException
        """

        if Person.query.check_if_already_exist_by_id_number(
                self.person.identity_number):
            raise FlaskProjectLogException(
                Status.status_id_number_already_exist())

        if self.person.mother_id is not None:
            mother = PersonController.get_one(
                self.person.mother_id)

            if mother.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.person.father_id is not None:
            father = PersonController.get_one(
                self.person.father_id)

            if father.person is None:
                raise FlaskProjectLogException(
                    Status.status_person_not_exist())

        if self.person.district is not None:
            district = DistrictController.get_one(
                self.person.district)

            if district.district is None:
                raise FlaskProjectLogException(
                    Status.status_district_not_exist())

        if self.person.religion is not None:
            religion = ListItemController.get_one(
                self.person.religion)

            if religion.list_item is None:
                raise FlaskProjectLogException(
                    Status.status_list_item_not_exist())

        self.person.add()
        self.person.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating persons
        :return: Status object or raise FlaskProjectLogException
        """

        person = Person.query.get_one(self.person.id)

        if person is None:
            raise FlaskProjectLogException(
                Status.status_person_not_exist())

        if Person.query.check_if_id_number_is_taken(
                person.id, self.person.identity_number):
            raise FlaskProjectLogException(
                Status.status_id_number_already_exist())

        person.first_name = self.person.first_name
        person.last_name = self.person.last_name
        person.maiden_name = self.person.maiden_name
        person.birth_date = self.person.birth_date
        person.identity_number = self.person.identity_number
        person.father_id = self.person.father_id
        person.mother_id = self.person.mother_id
        person.district = self.person.district
        person.religion = self.person.religion
        person.update()
        person.commit_or_rollback()

        self.person = person

        return Status.status_update_success().__dict__

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        """
        Method used for setting persons status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a person by identifier
        :param identifier: Extras Person identifier
        :return: PersonController object
        """
        return cls(person=Person.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get a person by identifier
        :param identifier: Person identifier
        :return: Dict object
        """
        return PersonController.__custom_sql(
            Person.query.get_one_details(identifier))

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching persons with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_search(search):
        """
        Method for searching persons
        :param search: Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all persons by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
        # Person.status == Person.STATUSES['active'])

        first_name = kwargs.get('first_name', None)
        last_name = kwargs.get('last_name', None)
        maiden_name = kwargs.get('maiden_name', None)
        birth_date = kwargs.get('birth_date', None)
        identity_number = kwargs.get('identity_number', None)
        father_id = kwargs.get('father_id', None)
        mother_id = kwargs.get('mother_id', None)
        district = kwargs.get('district', None)
        religion = kwargs.get('religion', None)

        if first_name:
            filter_main = and_(
                filter_main, Person.first_name.ilike('%' + first_name + '%'))

        if last_name:
            filter_main = and_(
                filter_main, Person.last_name.ilike('%' + last_name + '%'))

        if maiden_name:
            filter_main = and_(
                filter_main, Person.maiden_name.ilike('%' + maiden_name + '%'))

        if birth_date:
            filter_main = and_(
                filter_main, Person.birth_date.ilike('%' + birth_date + '%'))

        if identity_number:
            filter_main = and_(
                filter_main, Person.identity_number.ilike('%' + identity_number + '%'))

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

        data = Person.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(PersonController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.Person)
            mother = Person.query.filter_by(id=row_data.Person.mother_id).first()
            father = Person.query.filter_by(id=row_data.Person.father_id).first()
            return_dict['mother'] = obj_to_dict(mother)
            return_dict['father'] = obj_to_dict(father)
            return_dict['district'] = obj_to_dict(row_data.District)
            return return_dict
        return None
