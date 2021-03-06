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
    def status_archdiocese_already_exist(cls):
        """
        :return: cls(-1, 'This archdiocese already exist')
        """
        return cls(-1, 'This archdiocese already exist')

    @classmethod
    def status_archdiocese_not_exist(cls):
        """
        :return: cls(-1, 'This archdiocese does not exist')
        """
        return cls(-1, 'This archdiocese does not exist')

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
    def status_list_already_exist(cls):
        """
        :return: cls(-1, 'This list already exists')
        """
        return cls(-1, 'This list already exists')

    @classmethod
    def status_list_not_exist(cls):
        """
        :return: cls(-1, 'This list does not exist')
        """
        return cls(-1, 'This list does not exist')

    @classmethod
    def status_list_item_not_exist(cls):
        """
        :return: cls(-1, 'This list item does not exist')
        """
        return cls(-1, 'This list item does not exist')

    @classmethod
    def status_value_already_exists_in_list(cls):
        """
        :return: cls(-1, 'This value already exists in list')
        """
        return cls(-1, 'This value already exists in list')

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

    @classmethod
    def status_id_number_already_exist(cls):
        """
        :return: cls(-1, 'Person with that identity number already exists!')
        """
        return cls(-1, 'Person with that identity number already exists!')

    @classmethod
    def status_person_not_exist(cls):
        """
        :return: cls(-1, 'This person does not exist')
        """
        return cls(-1, 'This person does not exist')

    @classmethod
    def status_identity_number_already_exist(cls):
        """
        :return: cls(-1, 'Person with that identity number already exists in registry!')
        """
        return cls(-1, 'Person with that identity number already exists in registry!')

    @classmethod
    def status_counter_already_exist(cls):
        """
        :return: cls(-1, 'This counter already exists')
        """
        return cls(-1, 'This counter already exists')

    @classmethod
    def status_note_not_exist(cls):
        """
        :return: cls(-1, 'This note does not exist')
        """
        return cls(-1, 'This note does not exist')

    @classmethod
    def status_baptism_not_exist(cls):
        """
        :return: cls(-1, 'This baptism does not exist')
        """
        return cls(-1, 'This baptism does not exist')

    @classmethod
    def status_document_not_exist(cls):
        """
        :return: cls(-1, 'This document does not exist')
        """
        return cls(-1, 'This document does not exist')

    @classmethod
    def status_death_not_exist(cls):
        """
        :return: cls(-1, 'This registry of death does not exist')
        """
        return cls(-1, 'This registry of death does not exist')

    @classmethod
    def status_chrism_not_exist(cls):
        """
        :return: cls(-1, 'This chrism note does not exist')
        """
        return cls(-1, 'This chrism note does not exist')

    @classmethod
    def status_marriage_not_exist(cls):
        """
        :return: cls(-1, 'This marriage does not exist')
        """
        return cls(-1, 'This marriage does not exist')

    @classmethod
    def status_marriage_already_exists(cls):
        """
        :return: cls(-1, 'This registry of marriage already exists')
        """
        return cls(-1, 'This registry of marriage already exists')

    @classmethod
    def status_person_extra_info_already_exists(cls):
        """
        :return: cls(-1, 'This person already has extra info')
        """
        return cls(-1, 'This person already has extra info')

    def repr_print(self):
        return {
            "errorCode": self.errorCode,
            "description": self.description,
        }
