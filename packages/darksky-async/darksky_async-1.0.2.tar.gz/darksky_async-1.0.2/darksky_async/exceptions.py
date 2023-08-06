class DarkskyError(Exception):
    """
    Generic exception that this libary with throw if
    there is no sub exception
    """
    pass

class LocationNotFound(DarkskyError):
    """
    Exception for when a request doesnt find a location
    for the latitude, longitude pair
    """
    pass