"""
Utils Class
"""

import pytz
from datetime import datetime, timedelta


class Datetime_Utils():

    def __init__(self, tz="UTC", diff_days=0):
        dt = datetime.now(pytz.timezone(tz))

        if diff_days > 0:
            dt += timedelta(days=diff_days)
        elif diff_days < 0:
            dt -= timedelta(days=(-1 * diff_days))
        self.__dt = dt

    def iso(self):
        return self.__dt.isoformat()

    def format(self, format):
        return self.__dt.strftime(format)
