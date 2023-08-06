from datetime import datetime
from .utils import to_timezone

class Alert():
    __slots__ = (
        'description',
        'expires',
        'expiresLocal',
        'regions',
        'severity',
        'time',
        'timeLocal',
        'title',
        'uri'
    )
    def __init__(self, forecast, **data):
        # since we have defined what we expect in slots,
        # we cant add more information without editing slots
        for k, v in data.items():
            if k in ('expires', 'time'):
                v = datetime.utcfromtimestamp(v)
                setattr(self, k + 'Local', to_timezone(v, forecast.timezone))

            setattr(self, k, v)