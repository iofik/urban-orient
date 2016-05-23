from functools import total_ordering
from .util import attr_to_dict

@total_ordering
class Attraction(object):
    Name = "памятники"
    XPath = "/osm/node/tag[@k='tourism' and @v='attraction']/.."

    def __init__(self, elem):
        attr = attr_to_dict(elem)
        self.name = attr['name']
        self.lat = elem.attrib['lat']
        self.lon = elem.attrib['lon']

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '{0.name: <40} ({0.lat}, {0.lon})'.format(self)

    def update(self, other):
        raise KeyError
