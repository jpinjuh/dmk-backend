from sqlalchemy import and_

from ... import State, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict


class StateController(BaseController):

    def __init__(self, state=State()):
        self.state = state

    def create(self):
        """
        Method used for creating states
        :return: Status object or raise FlaskProjectLogException
        """

        if State.query.check_if_already_exist_by_name(
                self.state.name):
            raise FlaskProjectLogException(
                Status.status_state_already_exist())

        self.state.add()
        self.state.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        """
        Method used for updating states
        :return: Status object or raise FlaskProjectLogException
        """

        state = State.query.get_one(self.state.id)

        if state is None:
            raise FlaskProjectLogException(
                Status.status_state_not_exist())

        if State.query.check_if_name_is_taken(
                state.id, self.state.name):
            raise FlaskProjectLogException(
                Status.status_state_already_exist())

        state.name = self.state.name
        state.update()
        state.commit_or_rollback()

        self.state = state

        return Status.status_update_success().__dict__

    def inactivate(self):
        """
        Method used for setting states status to inactive (0)
        :return: Status object or raise FlaskProjectLogException
        """
        state = State.query.get_one(self.state.id)

        if state is None:
            raise FlaskProjectLogException(
                Status.status_state_not_exist())

        state.status = State.STATUSES['inactive']

        state.update()
        state.commit_or_rollback()

        self.state = state

        return Status.status_successfully_processed().__dict__

    def activate(self):
        """
        Method used for setting states status to active (1)
        :return: Status object or raise FlaskProjectLogException
        """
        state = State.query.get_one(self.state.id)

        if state is None:
            raise FlaskProjectLogException(
                Status.status_state_not_exist())

        if State.query.check_if_name_is_taken(
                state.id, self.state.name):
            raise FlaskProjectLogException(
                Status.status_state_already_exist())

        state.status = State.STATUSES['active']

        state.update()
        state.commit_or_rollback()

        self.state = state

        return Status.status_successfully_processed().__dict__

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a state by identifier
        :param identifier: Extras State identifier
        :return: StateController object
        """

        return cls(state=State.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        """
        Use this method to get a a state by identifier
        :param identifier: State identifier
        :return: Dict object
        """
        state = State.query.get_one(identifier)

        if state is not None:
            return obj_to_dict(state)

    @staticmethod
    def list_autocomplete(search):
        """
        Method for searching states with autocomplete
        :param search: Data for search
        :return: List of dicts
        """
        list_data = []
        if search:
            state = State.query.autocomplete_by_name(search)
            for i in state:
                list_data.append(obj_to_dict(i))

        return list_data

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        """
        Method for getting all states by filter_data in pagination form
        :return: dict with total, data and status
        """

        filter_main = and_()
            #State.status == State.STATUSES['active'])

        name = kwargs.get('name', None)

        if name:
            filter_main = and_(
                filter_main, State.name.ilike('%'+name+'%'))

        data = State.query.filter(
            filter_main).order_by(State.created_at.asc()).paginate(
            page=start, error_out=False, per_page=limit)

        total = data.total
        list_data = []

        for i in data.items:
            list_data.append(obj_to_dict(i))

        return dict(
            status=Status.status_successfully_processed().__dict__,
            total=total, data=list_data)
