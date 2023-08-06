
def toElementTree(etreeClass, bachDocument, parent=None, nsmap=None):
    # nsmap is a map of namespaces
    # e.g. {'xi': 'http://www.w3.org/2001/XInclude'}

    label, attributes, values = \
        bachDocument.label, bachDocument.attributes, bachDocument.children
    
    prefix = None
    if (":" in label) and nsmap:
        # e.g. "xi:include" => "xi", "include"
        prefix, label = label.split(":", maxsplit=1)
        label = etreeClass.QName(nsmap.get(prefix), label)

    if parent is not None:
        e = etreeClass.SubElement(parent, label)
    else:
        e = etreeClass.Element(label)
    
    for k,v in attributes.items():
        e.set(k, v)

    lastElement = e
    for i in values:
        if type(i) is str:
            if lastElement == e:
                if lastElement.text:
                    lastElement.text += ' ' + i
                else:
                    lastElement.text = i
            else:
                if lastElement.tail:
                    lastElement.tail += ' ' + i
                else:
                    lastElement.tail = i
        else:
            e2 = toElementTree(etreeClass, i, e, nsmap)
            lastElement = e2
    
    return e
