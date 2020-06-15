from sqlalchemy import and_

from ... import ListItem, FlaskProjectLogException, List
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict



class ListItemController(BaseController):

    def __init__(self, list_item=ListItem()):
        self.list_item = list_item

    def create(self):
        """
        Method used for creating list items
        :return: Status object or raise FlaskProjectLogException
        """

        if ListItem.query.check_if_value_already_exist_in_list(
                self.list_item.list_id, self.list_item.value):
            raise FlaskProjectLogException(
                Status.status_value_already_exists_in_list())

        self.list_item.add()
        self.list_item.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        return cls(list_item=ListItem.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
       Use this method to get an list item by identifier
       :param identifier: List item identifier
       :return: Dict object
       """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching list items with autocomplete
        :param search:Data for search
        :return: List of dicts
        """
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all listItems by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()

        list_value = kwargs.get('list_value', None)
        description = kwargs.get('description', None)
        auxiliary_description = kwargs.get('auxiliary_description', None)
        list_id = kwargs.get('list_id', None)

        if list_value:
            filter_main = and_(
                filter_main, ListItem.value.ilike('%' + list_value + '%'))

        if description:
            filter_main = and_(
                filter_main, ListItem.description.ilike('%' + description + '%'))

        if auxiliary_description:
            filter_main = and_(
                filter_main, ListItem.auxiliary_description == auxiliary_description)

        if list_id:
            filter_main = and_(
                filter_main, List.id == list_id)

        data = ListItem.query.get_all_by_filter(filter_main).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(ListItemController.__custom_sql(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)

    @staticmethod
    def __custom_sql(row_data):
        if row_data is not None:
            return_dict = obj_to_dict(row_data.ListItem)
            return_dict['list'] = obj_to_dict(row_data.List)
            return return_dict
        return None

    @staticmethod
    def get_list_items(list_id, current_user_district):

        list_data = []
        if list_id:
            list_items = ListItem.query.get_list_items_by_user_district(list_id, current_user_district)
            for i in list_items:
                list_data.append(ListItemController.__custom_sql(i))
            list_items = ListItem.query.get_list_items_by_other_districts(list_id, current_user_district)
            for i in list_items:
                list_data.append(ListItemController.__custom_sql(i))

        return list_data

