from sqlalchemy import and_

from ... import Counter, FlaskProjectLogException
from ...controllers.base_controller import BaseController
from ...general import Status, obj_to_dict
import datetime


class CounterController(BaseController):

    def __init__(self, counter=Counter()):
        self.counter = counter

    def create(self):
        """
        Method used for creating counter
        :return: Status object or raise FlaskProjectLogException
        """

        if Counter.query.check_if_already_exist_by_name(
                self.counter.name):
            raise FlaskProjectLogException(
                Status.status_counter_already_exist())

        self.counter.add()
        self.counter.commit_or_rollback()

        return Status.status_successfully_inserted().__dict__

    def alter(self):
        raise NotImplementedError("To be implemented")

    def inactivate(self):
        raise NotImplementedError("To be implemented")

    def activate(self):
        raise NotImplementedError("To be implemented")

    @classmethod
    def get_one(cls, identifier):
        """
        Use this method to get a counter by identifier
        :param identifier: Extras State identifier
        :return: CounterController object
        """

        return cls(counter=Counter.query.get_one(identifier))

    @staticmethod
    def get_one_details(identifier):
        raise NotImplementedError("To be implemented")

    def check_restart(self):
        """
        Call this method to restart counter to start_from value
        :return:
        """
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if self.counter.restart_time is None:
            self.counter.restart_time = datetime.datetime.now()
        if self.counter.restart_on is None:
            return self
        elif self.counter.restart_on == "$d":
            if self.counter.day == day and (
                    self.counter.restart_time + datetime.timedelta(days=1)) < datetime.datetime.now():
                try:
                    self.counter.restart_time = datetime.datetime.now().date()
                    self.counter.value = self.counter.start_from
                    self.counter.day = day
                    self.counter.month = month
                    self.counter.year = year
                    self.counter.add()
                    self.counter.commit_or_rollback()
                except Exception as e:
                    raise FlaskProjectLogException(Status(-101, str(e)).__dict__)
        elif self.counter.restart_on == "$m":
            if self.counter.month == month and (
                    self.counter.restart_time + datetime.timedelta(days=1)) < datetime.datetime.now():
                try:
                    self.counter.restart_time = datetime.datetime.now().date()
                    self.counter.value = self.counter.start_from
                    self.counter.day = day
                    self.counter.month = month
                    self.counter.year = year
                    self.counter.add()
                    self.counter.commit_or_rollback()
                except Exception as e:
                    raise FlaskProjectLogException(Status(-101, str(e)).__dict__)
        elif self.counter.restart_on == "$y":
            if self.counter.year == year and (
                    self.counter.restart_time + datetime.timedelta(days=1)) < datetime.datetime.now():
                try:
                    self.counter.restart_time = datetime.datetime.now().date()
                    self.counter.value = self.counter.start_from
                    self.counter.day = day
                    self.counter.month = month
                    self.counter.day = day
                    self.counter.add()
                    self.counter.commit_or_rollback()
                except Exception as e:
                    raise FlaskProjectLogException(Status(-101, str(e)).__dict__)
        return

    def replace_expression(self):
        """
        Call this method if you want custom counter defined in expression
        :return:
        """
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        expression = self.counter.expression.replace("$c", self.counter.value)
        expression = expression.replace("$d", str(day))
        expression = expression.replace("$m", str(month))
        expression = expression.replace("$y", str(year))
        return expression

    @staticmethod
    def generate(counter_id):
        """
        Use this method to generate new counter value
        :param counter_id: counter identifier unique
        :type counter_id: uuid
        :return: counter value or None
        :rtype: String
        """
        # Broj pokusaja dohvata brojaca
        max_repeat = 5
        counter_obj = CounterController.get_one(counter_id)

        if counter_obj.counter is None:
            return None
        # Ako nije definiran brojac
        if counter_obj.counter.value is None:
            # Ako je barem definiran start_from
            if counter_obj.counter.start_from is not None:
                counter_obj.counter.value = str(counter_obj.counter.start_from)
                try:
                    counter_obj.counter.add()
                    counter_obj.counter.commit_or_rollback()
                except Exception as e:
                    raise FlaskProjectLogException(Status(-101, str(e)).__dict__)
                # Ako postoji neki izraz
                if counter_obj.counter.expression is not None:
                    counter_obj.check_restart()
                    return counter_obj.replace_expression()
                # Ako ne postoji izraz
                else:
                    counter_obj.check_restart()
                    return counter_obj.counter.value
            # Ako nisu definirani brojac i start_from
            else:
                return None
        # Ako je definiran brojac
        else:
            for i in range(max_repeat):
                counter_obj.counter.value = int(counter_obj.counter.value) + 1
                try:
                    counter_obj.counter.add()
                    counter_obj.counter.commit_or_rollback()
                    break
                except Exception as e:
                    if i != (max_repeat - 1):
                        counter_obj.counter.value = int(counter_obj.counter.value) - 1
                        continue
                    raise FlaskProjectLogException(Status(-101, str(e)).__dict__)
            if counter_obj.counter.expression is not None:
                counter_obj.check_restart()
                return counter_obj.replace_expression()
            else:
                counter_obj.check_restart()
                return counter_obj.counter.value

    @staticmethod
    def list_autocomplete(search):
        raise NotImplementedError("To be implemented")

    @staticmethod
    def get_list_pagination(start, limit, **kwargs):
        raise NotImplementedError("To be implemented")
