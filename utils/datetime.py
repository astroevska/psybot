from datetime import date, datetime


def datetimeToDateStr(dt: datetime) -> str:
    return str(dt.date())

def strToDate(dateString: str) -> date:
    try:
        return datetime.strptime(dateString, '%Y-%m-%d').date()
    except:
        return date.today()