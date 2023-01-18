from datetime import date, datetime, timedelta
from dateutil import parser


def datetimeToDateStr(dt: datetime) -> str:
    return str(dt.date())


def strToDate(dateString: str) -> date:
    try:
        return datetime.strptime(dateString, '%Y-%m-%d').date()
    except:
        return date.today()


def nextDateByPeriod(period: str, currentDT = datetime.now()):
    if period == 'day':
        return parser.parse(str(currentDT + timedelta(days=1)))
    elif period == 'week':
        return parser.parse(str(currentDT + timedelta(weeks=1)))
    elif period == '2weeks':
        return parser.parse(str(currentDT + timedelta(weeks=2)))
    elif period == 'month':
        return parser.parse(str(currentDT + timedelta(days=30)))
