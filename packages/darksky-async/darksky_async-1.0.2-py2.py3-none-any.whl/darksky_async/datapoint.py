from datetime import datetime
from .utils import to_timezone

class DataPoint():
    # here we go
    __slots__ = (
        'apparentTemperature',
        'apparentTemperatureHigh',
        'apparentTemperatureHighTime',
        'apparentTemperatureHighTimeLocal',
        'apparentTemperatureLow',
        'apparentTemperatureLowTime',
        'apparentTemperatureLowTimeLocal',
        'apparentTemperatureMax',
        'apparentTemperatureMaxTime',
        'apparentTemperatureMaxTimeLocal',
        'apparentTemperatureMin',
        'apparentTemperatureMinTime',
        'apparentTemperatureMinTimeLocal',
        'cloudCover',
        'dewPoint',
        'humidity',
        'icon',
        'moonPhase',
        'nearestStormBearing',
        'nearestStormDistance',
        'ozone',
        'precipAccumulation',
        'precipIntensity',
        'precipIntensityError',
        'precipIntensityMax',
        'precipIntensityMaxTime',
        'precipIntensityMaxTimeLocal',
        'precipType',
        'precipProbability',
        'pressure',
        'summary',
        'sunriseTime',
        'sunriseTimeLocal',
        'sunsetTime',
        'sunsetTimeLocal',
        'temperature',
        'temperatureHigh',
        'temperatureHighTime',
        'temperatureHighTimeLocal',
        'temperatureLow',
        'temperatureLowTime',
        'temperatureLowTimeLocal',
        'temperatureMax',
        'temperatureMaxTime',
        'temperatureMaxTimeLocal',
        'temperatureMin',
        'temperatureMinTime',
        'temperatureMinTimeLocal',
        'time',
        'timeLocal',
        'uvIndex',
        'uvIndexTime',
        'uvIndexTimeLocal',
        'visibility',
        'windBearing',
        'windGust',
        'windGustTime',
        'windGustTimeLocal',
        'windSpeed'
    )
    def __init__(self, forecast, **optional_params):
        for key, value in optional_params.items():
            if key.lower().endswith('time'):
                value = datetime.utcfromtimestamp(value)
                setattr(self, key + 'Local', to_timezone(value, forecast.timezone))
            setattr(self, key, value)
