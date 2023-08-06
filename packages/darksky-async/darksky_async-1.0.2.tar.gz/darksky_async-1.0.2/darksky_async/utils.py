import pytz
from datetime import datetime

def to_timezone(dt, timezone):
    """
    Timezone converter based on pytz
    Originally used in WeatherBot but changed to work for DarkSkyAsync
    """
    if isinstance(dt, int):
        dt = datetime.utcfromtimestamp(dt)

    return dt.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone(timezone))