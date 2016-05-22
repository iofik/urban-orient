def attr_to_dict(elem):
    return { t.attrib['k']:t.attrib['v'] for t in elem.xpath('./tag') }
