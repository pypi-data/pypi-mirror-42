import pytz
from dateutil import tz
from datetime import datetime, date, timedelta
from jsonpickle.handlers import BaseHandler


class MongoDatetimeHandler(BaseHandler):
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fffZ'
    """
    Custom handler for datetime objects
    """
    MICROSECONDS_KEY = 'microsecond'

    def flatten(self, obj, data):
        pickler = self.context
        if not pickler.unpicklable:
            return obj
        if isinstance(obj, datetime):
            data['microsecond'] = obj.microsecond
            if obj.tzinfo:
                data['tzinfo_zone'] = obj.tzinfo.zone

        data['inner_date'] = obj

        return data

    def restore(self, data):
        utc_timezone = tz.gettz('UTC')
        original_datetime = data['inner_date']
        if 'microsecond' in data:
            original_datetime += timedelta(microseconds=data['microsecond']
                                                        - data['inner_date'].microsecond)

        if 'tzinfo_zone' in data:
            original_timezone = pytz.timezone(data['tzinfo_zone'])
            original_datetime = original_datetime.replace(tzinfo=utc_timezone)
            original_datetime = original_datetime.astimezone(original_timezone)
        return original_datetime


class MongoDateHandler(BaseHandler):
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fffZ'
    """
    Custom handler for date objects
    """

    def flatten(self, obj, data):
        pickler = self.context
        if not pickler.unpicklable:
            return obj

        date_as_dt = datetime(obj.year,
                              obj.month,
                              obj.day)
        data['inner_date'] = date_as_dt
        return data

    def restore(self, data):
        original_datetime = data['inner_date']
        return original_datetime.date()
