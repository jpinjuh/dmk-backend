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
    def status_test_category_already_exist(cls):
        """
        :return: cls(-1, 'This category already exist')
        """
        return cls(-1, 'This category already exist')

    @classmethod
    def status_test_category_not_exist(cls):
        """
        :return: cls(-1, 'This category does not exist')
        """
        return cls(-1, 'This category does not exist')

    @classmethod
    def status_test_film_not_exist(cls):
        """
        :return: cls(-1, 'This film does not exist')
        """
        return cls(-1, 'This film does not exist')

    def repr_print(self):
        return {
            "errorCode": self.errorCode,
            "description": self.description,
        }
