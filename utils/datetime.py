from datetime import date, datetime

from constants.config import TODAY_DATE


def datetimeToDateStr(dt: datetime) -> str:
    return str(dt.date())

def strToDate(dateString: str) -> date:
    try:
        return datetime.strptime(dateString, '%Y-%m-%d').date()
    except:
        return TODAY_DATE