from .sources import find_source

class Flags():
    def __init__(self, **data):
        for key, value in data.items():
            if key == 'sources':
                # special case handling
                sources = []
                for source_code in value:
                    # dont add anything we dont recognise
                    try:
                        sources.append(find_source(source_code))
                    except:
                        pass
                value = sources

            setattr(self, key, value)