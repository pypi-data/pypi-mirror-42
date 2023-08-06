import asyncio
from .http import HTTPClient
from .utils import to_timezone

class Client():
    def __init__(self, key, loop=None):
        self.http = HTTPClient(loop=loop)
        self.key = key

    async def forecast(self, latitude, longitude, **optional_params):
        """
        Gets the weather for a latitude, longitude pair

        Use the get_dict kwarg if you wish to get the raw dict from DarkSky
        for caching or saving purposes
        """

        return await self.http.get(self.key, latitude, longitude, **optional_params)

async def forecast(key, lat, lon, **optional_params):
    """
    For those who wish to just get the weather information
    from a lat, lon pair. This creates a new DarkSky object
    every time this is called. If you are running this function more than once,
    it is adviced that you create the client and save it to a variable insted of calling this
    function

    See this for more information:
    """
    client = Client(key)
    ret = await client.forecast(lat, lon, **optional_params)
    return ret