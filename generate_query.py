# Method receives the options selected by the user and generates the TIGER Search Query

from collections import defaultdict
from pprint import pprint

queryItems = defaultdict(list)


def getQuery(options):
    final = defaultdict(dict)
    for k,v in options.items():
        temp = k.split(" ")
        key = temp[0]
        final[key][temp[1]] = v
    pprint(final)
    query = ""
    count = 1
    for key, value in final.items():
        term1 = ""
        term2 = ""
        term3 = ""
        term4 = ""
        term5 = ""
        for k,v in value.items():
            if k == "rel":
                term3 = "%s" %v
            if k == "head":
                term1 = "word = \"%s\"" %v
            if k == "head_label":
                term2 = "pos = \"%s\"" %v
            if k == "dep":
                term4 = "word = \"%s\"" %v
            if k == "dep_label":
                term5 = "pos = \"%s\"" %v

# A: Head part, C: relation part, B: Dependent part
        if term1 == "" and term2 == "":
            A = ""
        elif term1 == "":
            A = " [" + term2 + "] "
        elif term2 == "":
            A = " [" + term1 + "] "
        elif term1 != "" and term2 != "":
            A = " [" + term1 + " & " + term2 + "] "

        if term4 == "" and term5 == "":
            B = ""
        elif term4 == "":
            B = " [" + term5 + "] "
        elif term5 == "":
            B = " [" + term4 + "] "
        elif term4 != "" and term5 != "":
            B = " [" + term4 + " & " + term5 + "] "

        C = term3

        if A != "" and B != "":
            x = A + " >" + term3 + B
        elif (A == "" or B == "") and C == "":
            x = A + B
        if C != "":
            if A == "" and B != "":
                x = "#n%d >"%count + C + B
            if B == "" and A != "":
                x = A + " >" + C + " #n%d"%count
            if A == "" and B == "":
                x = "#n%d >"%count +C + " #m%d"%count
        count+=1
        query += "("+x+")" + "\n& "
    index = query.rfind("\n&")
    return query[:index]