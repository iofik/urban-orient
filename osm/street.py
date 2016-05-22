from functools import total_ordering
from .util import attr_to_dict

def name_to_sorting(name):
    l = name.split()
    idx = next(filter(lambda i: not l[i].islower(), range(len(l))), None)
    if idx is not None:
        l = l[idx:] + l[:idx]
    return ' '.join(l)

@total_ordering
class Street(object):
    Name = "улицы"
    XPath = "/osm/way/tag[@k='highway']/../tag[@k='name']/.."

    def __init__(self, elem):
        attr = attr_to_dict(elem)

        self.name     = name_to_sorting(attr['name']) # should be same as 'sorting_name'
        self.old_name = attr.get('old_name') or attr.get('omkum:old_name')

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{s.name}  //  {s.old_name}".format(s=self) if self.old_name else self.name

    def update(self, other):
        if self != other:
            raise Exception("merging different streets")
        if not self.old_name:
            self.old_name = other.old_name
        elif other.old_name and self.old_name != other.old_name:
            if not hasattr(self, '_old_names'):
                self._old_names = { self.old_name }
            if other.old_name not in self._old_names:
                self._old_names.add(other.old_name)
                self.old_name += " / " + other.old_name
