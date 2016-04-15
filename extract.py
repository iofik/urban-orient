#!/usr/bin/env python3

import sys
from functools import total_ordering
from lxml import etree
from os.path import basename

def attr_to_dict(elem):
    return { t.attrib['k']:t.attrib['v'] for t in elem.xpath('./tag') }

def name_to_sorting(name):
    l = name.split()
    idx = next(filter(lambda i: not l[i].islower(), range(len(l))), None)
    if idx is not None:
        l = l[idx:] + l[:idx]
    return ' '.join(l)

@total_ordering
class Street(object):
    def __init__(self, elem):
        attr = attr_to_dict(elem)

        self.name     = name_to_sorting(attr['name']) # should be same as 'sorting_name'
        self.old_name = attr.get('old_name') or attr.get('omkum:old_name')

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

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

def main(fname):
    osm = etree.parse(fname)

    streets = {}
    for el in osm.xpath("/osm/way/tag[@k='highway']/../tag[@k='name']/.."):
        s = Street(el)
        s2 = streets.get(s.name)
        if s2:
            s2.update(s)
        else:
            streets[s.name] = s

    for n,s in sorted(streets.items()):
        print("{s.name}  //  {s.old_name}".format(s=s) if s.old_name else s.name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 {0} <map.osm>".format(basename(sys.argv[0])))
    else:
        main(sys.argv[1])
