import asyncio
import aiohttp

from .datablock import DataBlock
from .forecast import Forecast
from .backoff import ExponentialBackoff
from .exceptions import LocationNotFound, DarkskyError

API_BASE_URL = 'https://api.darksky.net/forecast'

class HTTPClient():
    def __init__(self, loop=None, session=None):
        """
        Create a HTTP session using the loop
        """
        # check if the loop exists, if not, create the loop from
        # the default
        self.loop = loop if loop else asyncio.get_event_loop()
        self._session = session if session else aiohttp.ClientSession(loop=self.loop)

    async def get(self, key, lat, lon, time=None, **optional_params):
        """
        Get data from DarkSky
        """
        if not time:
            url = f'{API_BASE_URL}/{key}/{lat},{lon}'
        else:
            url = ''
        
        params = {}
        for key, value in optional_params.items():
            if isinstance(value, list):
                value = ','.join(value)
            params[key] = value

        tries = 0
        backoff = ExponentialBackoff()

        while tries < 3:
            request = await self._session.request('GET', url, params=params)
            if request.status < 300:
                break
 
            if request.status in [500, 502]:
                # Unconditional retry
                to_sleep = backoff.delay()
                await asyncio.sleep(to_sleep)
                continue # restart the loop again

            tries += 1

        data = await request.json()
        if 'error' in data:
            # there was an error while handling this request
            if data['code'] == 400 and data['error'] == 'The given location is invalid.':
                raise LocationNotFound(data['error'])
            else:
                raise DarkskyError(data['error'])
                
        # sort the high level data into this list
        # this is to clean up the incoming dict so we can sort it 
        # into datablocks and points
        high_level = []
        for key in ['latitude', 'longitude', 'timezone']:
            high_level.append(data.get(key, None))
            del data[key]

        return Forecast(
            self,
            request.headers,
            *high_level,
            **data
        )