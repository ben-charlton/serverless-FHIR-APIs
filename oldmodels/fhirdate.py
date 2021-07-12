import sys
import logging
import isodate
import datetime

logger = logging.getLogger(__name__)
class FHIRDate(object):

    def __init__(self, jsonval=None):
        self.date = None
        if jsonval is not None:
            isstr = isinstance(jsonval, str)
            if not isstr:
                raise TypeError("Expecting string when initializing {}, but got {}"
                    .format(type(self), type(jsonval)))
            try:
                if 'T' in jsonval:
                    self.date = isodate.parse_datetime(jsonval)
                else:
                    self.date = isodate.parse_date(jsonval)
            except Exception as e:
                logger.warning("Failed to initialize FHIRDate from \"{}\": {}"
                    .format(jsonval, e))
        
        self.origval = jsonval
    
    def __setattr__(self, prop, value):
        if 'date' == prop:
            self.origval = None
        object.__setattr__(self, prop, value)
    
    @property
    def isostring(self):
        if self.date is None:
            return None
        if isinstance(self.date, datetime.datetime):
            return isodate.datetime_isoformat(self.date)
        return isodate.date_isoformat(self.date)
    
    @classmethod
    def with_json(cls, jsonobj):
        """ Initialize a date from an ISO date string.
        """
        isstr = isinstance(jsonobj, str)
        if isstr:
            return cls(jsonobj)
        
        if isinstance(jsonobj, list):
            return [cls(jsonval) for jsonval in jsonobj]
        
        raise TypeError("`cls.with_json()` only takes string or list of strings, but you provided {}"
            .format(type(jsonobj)))

    
    def as_json(self):
        if self.origval is not None:
            return self.origval
        return self.isostring