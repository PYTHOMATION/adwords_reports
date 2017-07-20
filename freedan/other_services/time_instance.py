import datetime

descriptive_weekdays = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday"
}


class TimeInstance:
    """ Time utility class providing a lot of often used functionality:
        - dates to strings
        - dates with certain offset
        - dates in adwords format
        - check if string is valid date
        - ...
    """
    def __init__(self, offset=0):
        self.datetime = datetime.datetime.now() + datetime.timedelta(offset)
        self.date = self.datetime.date()
        self.year = self.date.year
        self.month = self.date.month
        self.hour = self.datetime.hour
        self.last_hour = 23 if self.hour == 0 else self.hour - 1
        self.weekday = self.datetime.isoweekday()

        self.date_string = self.date.strftime("%Y-%m-%d")
        self.month_string = self.__two_character_string(self.month)
        self.hour_string = self.__two_character_string(self.hour)
        self.last_hour_string = self.__two_character_string(self.last_hour)
        self.weekday_descriptive = descriptive_weekdays[self.weekday]
        self.date_hour_string = "{date}_{hour}".format(date=self.date_string, hour=self.hour_string)
        self.year_month_string = "{year}-{month}".format(year=self.year, month=self.month_string)
        self.adwords_date_string = self.date_string.replace("-", "")

    @staticmethod
    def __two_character_string(number):
        """
        leading zero for 1-character numbers, i.e. 0 -> 00, 8 -> 08, 12 -> 12
        :param number: int
        :return: str
        """
        number_string = str(number).zfill(2)
        return number_string

    @staticmethod
    def is_date_string(date_text):
        """ Check if string is a valid date in YYYY-MM-DD format """
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False
