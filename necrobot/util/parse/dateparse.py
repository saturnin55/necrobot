import datetime
import pytz

import necrobot.exception
from dateutil import parser


class CustomParserInfo(parser.parserinfo):
    WEEKDAYS = [
        ('Mon', 'Monday'),
        ('Tue', 'Tues', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thurs', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday')
    ]


def parse_datetime(parse_str: str, timezone: pytz.timezone = pytz.utc) -> datetime.datetime:
    if parse_str.lower() == 'now':
        return pytz.utc.localize(datetime.datetime.utcnow())

    try:
        default_time = (pytz.utc.localize(datetime.datetime.utcnow()).astimezone(timezone))\
            .replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
        dateutil_parse = parser.parse(
            parse_str,
            default=default_time,
            fuzzy=True,
            dayfirst=False,
            yearfirst=False)
        if 'tomorrow' in parse_str:
            return timezone.localize(dateutil_parse + datetime.timedelta(days=1)).astimezone(pytz.utc)
        else:
            return timezone.localize(dateutil_parse).astimezone(pytz.utc)
    except ValueError:
        raise necrobot.exception.ParseException('Couldn\'t parse {0} as a time.'.format(parse_str))
    except OverflowError:
        raise necrobot.exception.ParseException(
            'That date is really just too big. (Like, so big it doesn\'t fit in an int value on this system.) '
            'Congratulations! Please try again.'
        )
