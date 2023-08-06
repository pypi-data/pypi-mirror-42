
from .datablock import DataBlock
from .datapoint import DataPoint
from .flag import Flags
from .alert import Alert

IS_DATABLOCK = [
    'minutely',
    'hourly',
    'daily'
]

class Forecast():
    __slots__ = (
        'currently',
        'minutely',
        'hourly',
        'daily',
        'alerts',
        'flags',
        'latitude',
        'longitude',
        'timezone',
        'headers',
        'raw',
        '_state'
    )
    def __init__(self, state, headers, latitude, longitude, timezone, **optional_params):
        self._state = state

        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.headers = headers # unprocessed
        self.raw = optional_params
        self.raw['latitude'] = latitude
        self.raw['longitude'] = longitude
        self.raw['timezone'] = timezone
        self.alerts = [] # set default as an empty list
        
        for key, value in optional_params.items():
            if key in IS_DATABLOCK:
                # we give the forecast object as the first arg because
                # we need the timezone information for the local param
                setattr(self, key, DataBlock(self, **value))
            elif key == 'currently':
                setattr(self, key, DataPoint(self, **value))
            elif key == 'alerts':
                # handle alerts array
                alerts = []
                for alert in value:
                    alerts.append(Alert(self, **alert))
                setattr(self, key, alerts)

            elif key == 'flags':
                setattr(self, key, Flags(**value))

    @property
    def total_cost(self):
        """
        Returns the amount due for this key per day
        Amount is in Dollars
        """
        if self.headers.get('X-Forecast-API-Calls', 0) < 1000:
            return 0
        else:
            return (self.headers.get('X-Forecast-API-Calls', 0) - 1000) / 0.0001