from datetime import datetime, timedelta

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%d-%b-%Y", "%d/%m/%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def days_between(d1, d2):
    if d1 and d2:
        return abs((d2 - d1).days)
    return None