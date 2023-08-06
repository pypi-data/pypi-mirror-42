from wikidata.client import Client
from wikidata.entity import Entity

from .validators import validate_wikidata_item

client = Client()


class WikidataEntity(Entity):
    '''
    Subclass Entity that implements pickle protocol
    '''

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.id == other
        if not isinstance(other, type(self)):
            raise TypeError(
                'expected an instance of {0.__module__}.{0.__qualname__}, '
                'not {1!r}'.format(type(self), other)
            )
        return other.id == self.id and self.client is other.client

    def __getstate__(self):
        return {'id': self.id}


def make_entity(value):
    validate_wikidata_item(value)
    return WikidataEntity(value, client)
