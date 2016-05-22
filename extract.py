#!/usr/bin/env python3

import sys
from lxml import etree
from os.path import basename
from osm.street import Street

def main(fname):
    osm = etree.parse(fname)

    for cls in [Street]:
        objs = {}
        for el in osm.xpath(cls.XPath):
            o = cls(el)
            try:
                objs[o].update(o)
            except KeyError:
                objs[o] = o

        print('  {0}  '.format(cls.Name.upper()).center(60, '='))
        for n,o in sorted(objs.items()):
            print(o)
        print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 {0} <map.osm>".format(basename(sys.argv[0])))
    else:
        main(sys.argv[1])
