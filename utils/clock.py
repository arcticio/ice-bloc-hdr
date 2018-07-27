# To change this template, choose Tools | Templates
# and open the template in the editor.


## http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/

import time

from datetime import datetime, timedelta, tzinfo
import re

months = {
  '01' : "Jan", '02' : "Feb", '03' : "Mar",
  '04' : "Apr", '05' : "May", '06' : "Jun",
  '07' : "Jul", '08' : "Aug", '09' : "Sep",
  '10' : "Oct", '11' : "Nov", '12' : "Dec",
}

class Clock(object):
  tick      = time.localtime(time.time())
  tick      = time.time()
  now       = datetime.now()
  today     = datetime.today()
  doy       = int(time.strftime("%j", time.localtime(time.time())))
  yesterday = datetime.today() - timedelta(1)
  yesterdoy = doy -1
  year      = int(time.strftime("%Y", time.localtime(time.time())))

  def deb(self):
    print "__Clock"
    print "tick:"   , type(Clock.tick).__name__ ,   Clock.tick
    print "now:"    , type(Clock.now).__name__,     Clock.now
    print "today:"  , type(Clock.today).__name__,   Clock.today
    print "dayISO:" , type(Clock.dateISO).__name__, Clock.dateISO

  def __init__(self, datum=None):

    if datum == None :
      self.date = datetime.today()
      self.datetime = datetime.now()
      self.dateISO = time.strftime("%Y-%m-%d", datetime.today().timetuple())

    elif type(Clock.today).__name__ == 'date' :
      self.date = datum

    elif self.isISO8601(datum) :
      datum = datum.split("-")
      self.date     = datetime.date(datetime(int(datum[0]), int(datum[1]), int(datum[2])))
      self.datetime = datetime(int(datum[0]), int(datum[1]), int(datum[2]))

    else :
      self.date = parse_date(datum)

    self.year = self.date.year
    self.doy  = (self.datetime - datetime(self.date.year, 1, 1)).days +1

  def UTC(self, format="%Y-%m-%d", diff=0, ) :
    return time.strftime(format, (datetime.utcnow() + timedelta(hours=diff)).timetuple())

  def isISO8601(self, something):

    ##http://www.cl.cam.ac.uk/~mgk25/iso-time.html

    try :
      if len(something) == 10 and len(something.split("-")) == 3 :
        return True
    except :
      return False
    return False

  def formatISO(self, isoDate="", format=""):

    ## http://docs.python.org/library/datetime.html#strftime-strptime-behavior
    if isoDate  == "" : isoDate = self.dateISO
    if format == "%b" : return months[isoDate.split("-")[1]]
    return time.strftime(format, datetime.strptime(isoDate, "%Y-%m-%d").timetuple())

  def fromStamp(self, stamp, diff=0):

    year  = int(time.strftime("%Y", time.localtime(time.time())))
    year0 = str(year)
    doy   = int(time.strftime("%j", time.localtime(time.time()))) + diff
    doy3  = str(doy).zfill(3)

    ## http://www.tutorialspoint.com/python/time_strftime.htm


    if stamp == "doy" :
      return doy3

    if stamp == "Last-Tue/YYYYMMDD" :
      d = datetime.today() - timedelta(days=self.date.weekday() -1)    
      return time.strftime("%Y%m%d", d.timetuple())

    if stamp == "now/tick" :
      return int(time.time() * 1000)

    if stamp == "now/month" :
      return time.strftime("%m", time.localtime(time.time()))

    if stamp == "now/day" :
      return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    if stamp == "now/day/no/-1" :
      return time.strftime("%Y%m%d", time.localtime(time.time() - 1 * 60*60*24))

    if stamp == "now/day/no/-2" :
      return time.strftime("%Y%m%d", time.localtime(time.time() - 2 * 60*60*24))

    if stamp == "YYYYMMDD" :
      return time.strftime("%Y%m%d", time.localtime(time.time() ))
      #~ return time.strftime("%Y%m%d", time.localtime(time.time() - 1 * 60*60*24))

    if stamp == "now/doy" :
      return time.strftime("%Y-%j", time.localtime(time.time()))

    if stamp == "year-doy-0" :
      return time.strftime("%Y-%j", time.localtime(time.time() - 0 * 60*60*24))
    if stamp == "year-doy-1" :
      return time.strftime("%Y-%j", time.localtime(time.time() - 1 * 60*60*24))
    if stamp == "year-doy-2" :
      return time.strftime("%Y-%j", time.localtime(time.time() - 2 * 60*60*24))
    if stamp == "year-doy-3" :
      return time.strftime("%Y-%j", time.localtime(time.time() - 3 * 60*60*24))
    if stamp == "year.doy-1" :
      return time.strftime("%Y.%j", time.localtime(time.time() - 1 * 60*60*24))
    if stamp == "yeardoy-1" :
      return time.strftime("%Y%j", time.localtime(time.time() - 1 * 60*60*24))

    if stamp == "yeardoy" :
      return year0 + doy3

    if stamp == "now/hour" :
      return time.strftime("%Y-%m-%d-%H", time.localtime(time.time()))

    if stamp == "now/minute" :
      return time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))

    if stamp == "yester/day" :
      return time.strftime("%Y-%m-%d", time.localtime(time.time() - 60*60*24))

    if stamp == "yester/doy" :
      return time.strftime("%Y-%j", time.localtime(time.time() - 60*60*24))

    if stamp == "pub/day" :
      return time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))


## http://code.google.com/p/pyiso8601/source/browse/trunk/iso8601/iso8601.py

"""ISO 8601 date time string parsing

Basic usage:
>>> import iso8601
>>> iso8601.parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.iso8601.Utc ...>)
>>>

"""



__all__ = ["parse_date", "ParseError"]

# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile(r"(?P<year>[0-9]{4})(-(?P<month>[0-9]{1,2})(-(?P<day>[0-9]{1,2})"
    r"((?P<separator>.)(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})(:(?P<second>[0-9]{2})(\.(?P<fraction>[0-9]+))?)?"
    r"(?P<timezone>Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?"
)
TIMEZONE_REGEX = re.compile("(?P<prefix>[+-])(?P<hours>[0-9]{2}).(?P<minutes>[0-9]{2})")

class ParseError(Exception):
    """Raised when there is a problem parsing a date string"""

# Yoinked from python docs
ZERO = timedelta(0)
class Utc(tzinfo):
    """UTC

    """
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
UTC = Utc()

class FixedOffset(tzinfo):
    """Fixed offset in hours and minutes from UTC

    """
    def __init__(self, offset_hours, offset_minutes, name):
        self.__offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

    def __repr__(self):
        return "<FixedOffset %r>" % self.__name

def parse_timezone(tzstring, default_timezone=UTC):
    """Parses ISO 8601 time zone specs into tzinfo offsets

    """
    if tzstring == "Z":
        return default_timezone
    # This isn't strictly correct, but it's common to encounter dates without
    # timezones so I'll assume the default (which defaults to UTC).
    # Addresses issue 4.
    if tzstring is None:
        return default_timezone
    m = TIMEZONE_REGEX.match(tzstring)
    prefix, hours, minutes = m.groups()
    hours, minutes = int(hours), int(minutes)
    if prefix == "-":
        hours = -hours
        minutes = -minutes
    return FixedOffset(hours, minutes, tzstring)

def parse_date(datestring, default_timezone=UTC):
    """Parses ISO 8601 dates into datetime objects

    The timezone is parsed from the date string. However it is quite common to
    have dates without a timezone (not strictly correct). In this case the
    default timezone specified in default_timezone is used. This is UTC by
    default.
    """
    if not isinstance(datestring, basestring):
        raise ParseError("Expecting a string %r" % datestring)
    m = ISO8601_REGEX.match(datestring)
    if not m:
        raise ParseError("Unable to parse date string %r" % datestring)
    groups = m.groupdict()
    tz = parse_timezone(groups["timezone"], default_timezone=default_timezone)
    if groups["fraction"] is None:
        groups["fraction"] = 0
    else:
        groups["fraction"] = int(float("0.%s" % groups["fraction"]) * 1e6)
    return datetime(int(groups["year"]), int(groups["month"]), int(groups["day"]),
        int(groups["hour"]), int(groups["minute"]), int(groups["second"]),
        int(groups["fraction"]), tz)

