# Method receives the options selected by the user and generates the TIGER Search Query

from collections import defaultdict
from pprint import pprint

queryItems = defaultdict(list)


def getQuery(options):
    finalQuery = "[ "
    queryTemp = []
    for k,v in options.items():
        temp = k.split(" ")
        key = temp[0]
        if "label" in temp[1]:
            x = "pos = \"%s\"" %v
        else:
            x = "word = \"%s\"" % v
        queryItems[key].append(x)
    #pprint(queryItems)

    for k,v in queryItems.items():
        temp = "["
        for x in v:
            if x != v[-1]:
                temp = temp + "%s & " %x
            else:
                temp = temp + "%s]" %x
        queryTemp.append(temp)
    for x in queryTemp:
        if x != queryTemp[-1]:
            finalQuery = finalQuery + "%s & " %x
        else:
            finalQuery = finalQuery + "%s ]" %x
    return finalQuery