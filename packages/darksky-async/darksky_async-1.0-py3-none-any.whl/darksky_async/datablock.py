from .datapoint import DataPoint

class DataBlock():
    __slots__ = ('_forecast', 'icon', 'summary', 'data')
    def __init__(self, forecast, icon, summary, data):
        self._forecast = forecast
        self.icon = icon
        self.summary = summary
        self.data = []
        for item in data:
            self.data.append(DataPoint(self._forecast, **item))
