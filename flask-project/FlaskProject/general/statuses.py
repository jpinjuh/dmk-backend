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
    def status_unsuccessfully_processed(cls):
        """
        :return: cls(200, 'Unsuccessfully processed')
        """
        return cls(-1, 'Unsuccessfully processed')

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
    def status_city_already_exist(cls):
        """
        :return: cls(-1, 'This city already exist')
        """
        return cls(-1, 'This city already exist')

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

    @classmethod
    def status_district_already_exist(cls):
        """
        :return: cls(-1, 'This district already exists')
        """
        return cls(-1, 'This district already exists')

    @classmethod
    def status_role_already_exist(cls):
        """
        :return: cls(-1, 'This role already exists')
        """
        return cls(-1, 'This role already exists')

    @classmethod
    def status_role_not_exist(cls):
        """
        :return: cls(-1, 'This role does not exist')
        """
        return cls(-1, 'This role does not exist')

    @classmethod
    def status_permission_already_exist(cls):
        """
        :return: cls(-1, 'This permission already exists')
        """
        return cls(-1, 'This permission already exists')

    @classmethod
    def status_permission_not_exist(cls):
        """
        :return: cls(-1, 'This permission does not exist')
        """
        return cls(-1, 'This permission does not exist')

    @classmethod
    def status_privilege_already_exist(cls):
        """
        :return: cls(-1, 'This privilege already exists')
        """
        return cls(-1, 'This privilege already exists')

    @classmethod
    def status_privilege_not_exist(cls):
        """
        :return: cls(-1, 'This privilege does not exist')
        """
        return cls(-1, 'This privilege does not exist')

    @classmethod
    def status_user_already_exist(cls):
        """
        :return: cls(-1, 'User with that username already exists.')
        """
        return cls(-1, 'User with that username already exists.')

    @classmethod
    def status_user_with_that_email_already_exist(cls):
        """
        :return: cls(-1, 'User with that email address already exists.')
        """
        return cls(-1, 'User with that email address already exists.')

    @classmethod
    def status_user_not_exist(cls):
        """
        :return: cls(-1, 'This user does not exist')
        """
        return cls(-1, 'This user does not exist')

    @classmethod
    def status_success(cls):
        """
        :return: cls(-1, 'Allowed access!')
        """
        return cls(-1, 'Allowed access!')

    @classmethod
    def status_access_denied(cls):
        """
        :return: cls(-1, 'Access denied!')
        """
        return cls(-1, 'Access denied!')

    @classmethod
    def status_pass_dont_match(cls):
        """
        :return: cls(-1, 'Passwords do not match!')
        """
        return cls(-1, 'Passwords do not match!')

    def repr_print(self):
        return {
            "errorCode": self.errorCode,
            "description": self.description,
        }
