
ALL_SOURCES = {
    'cmc': {
        'name': 'Canadian Meteorological Center'
    },
    'darksky': {
        'name': 'DarkSky',
        'url': 'https://darksky.net'
    },
    'ecpa': {
        'name': 'Environment and Climate Change Canada\'s Public Alert system',
        'url': 'https://weather.gc.ca/warnings/index_e.html',
        'availability': ['CAN']
    },
    'gfs': {
        'name': 'NOAA - Global Forecast System'
    },
    'hrrr': {
        'name': 'NOAA - High-resolution Rapid Refresh Model',
        'url': 'https://rapidrefresh.noaa.gov/hrrr/',
        'availability': ['USA']
    },
    'icon': {
        'name': 'German Meteorlogical Icosahedral Nonhydrostatic Model',
        'url': 'https://www.dwd.de/EN/research/weatherforecasting/num_modelling/01_num_weather_prediction_modells/icon_description.html'
    },
    'isd': {
        'name': 'NOAA - Integrated Surface Database',
        'notes': 'Available near populated areas globally for times greater than two weeks in the past.'
    },
    'madis': {
        'name': 'NOAA - Meteorological Assimilation Data Ingest System',
        'url': 'https://madis.ncep.noaa.gov/'
    },
    'meteoalarm': {
        'name': 'Meteoalarm weather alerting system',
        'url': 'https://meteoalarm.eu/',
        'availability': ['EU', 'ISR']
    },
    'nam': {
        'name': 'NOAA - North American Mesoscale Model',
        'availability': ['USA']
    },
    'nwspa': {
        'name': 'NOAA - Public Alert System',
        'url': 'https://alerts.weather.gov/'
    },
    'sref': {
        'name': 'NOAA - Short-Range Ensemble Forecast',
        'availability': ['USA']
    }
}
def find_source(source_code):
    source = ALL_SOURCES.get(source_code, {
        # default source
        'name': 'Unknown Source',
        'url': 'https://darksky.net/dev/docs/sources'
    })

    if not source:
        raise ValueError('Source id does not exist')
    
    source['id'] = source_code

    if 'availability' not in source:
        source['availability'] = 'global'
    if 'url' not in source:
        source['url'] = None

    class BaseSource(): 
        def __init__(self, **source):
            for k, v in source.items():
                setattr(self, k, v)

        def __str__(self):
            return self.name

        def __repr__(self):
            return f'<DarkSkySource id="{self.id}" name="{self.name}">'

    BaseSource.__name__ = source_code.lower()
    return BaseSource(**source)

