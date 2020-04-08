class Status:
    def __init__(self, error_code=None, description=None):
        self.errorCode = error_code
        self.description = description

    @classmethod
    def something_went_wrong(cls):
        """
        :return: cls(-1, 'Something went wrong')
        """
        return cls(-1, 'Something went wrong',)

    @classmethod
    def status_successfully_access_to_route(cls):
        """
        :return: cls(200, 'You have successfully accessed the route)
        """
        return cls(200, 'You have successfully accessed the route')

    @classmethod
    def status_successfully_inserted(cls):
        """
        :return: cls(200, 'Successfully inserted')
        """
        return cls(200, 'Successfully inserted')

    @classmethod
    def status_update_success(cls):
        """
        :return: cls(200, 'Successfully updated')
        """
        return cls(200, 'Successfully updated')

    @classmethod
    def status_successfully_processed(cls):
        """
        :return: cls(200, 'Successfully processed')
        """
        return cls(200, 'Successfully processed')

    @classmethod
    def status_connection_refuse(cls):
        """
        :return: cls(-1, 'Connection refuse')
        """
        return cls(-1, 'Connection refuse')

    @classmethod
    def status_token_required(cls):
        """
        :return: cls(-1, 'Token required')
        """
        return cls(-1, 'Token required')

    @classmethod

    def status_state_already_exist(cls):
        """
        :return: cls(-1, 'This state already exist')
        """
        return cls(-1, 'This state already exist')

    @classmethod
    def status_state_not_exist(cls):
        """
        :return: cls(-1, 'This state does not exist')
        """
        return cls(-1, 'This state does not exist')

    @classmethod
    def status_city_not_exist(cls):
        """
        :return: cls(-1, 'This city does not exist')
        """
        return cls(-1, 'This city does not exist')

    @classmethod
    def status_district_not_exist(cls):
        """
        :return: cls(-1, 'This district does not exist')
        """
        return cls(-1, 'This district does not exist')

    def status_role_already_exist(cls):
        """
        :return: cls(-1, 'This role already exist')
        """
        return cls(-1, 'This role already exist')

    @classmethod
    def status_role_not_exist(cls):
        """
        :return: cls(-1, 'This role does not exist')
        """
        return cls(-1, 'This role does not exist')

    def repr_print(self):
        return {
            "errorCode": self.errorCode,
            "description": self.description,
        }
