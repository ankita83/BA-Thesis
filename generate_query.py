# Method to generate the TIGER Search query from the options selected by the user

from collections import defaultdict
from pprint import pprint

# A: Head part, C: relation part, B: Dependent part
def getQuery(data):
    queryItems = defaultdict(list)

    for k,v in data.items():
        temp = k.split(":")
        key = temp[0]
        x = temp[1].split(" ")
        queryItems[key].append((x[0], x[1], v))

    #pprint(queryItems)
    count = 1
    finalQuery = ""
    for k,v in queryItems.items():
        #print v
        RHS = "#%s" %k
        A = ""
        str1 = ""
        str2 = ""
        for item in v:
            #print item
            if item[1] == "head":
                str1 = "word=\"%s\"" %item[2]
            if item[1] == "head_label":
                str2 = "pos=\"%s\"" %item[2]

        if str1 == "" and str2 == "":
            A = ""
        elif str2 == "" :
            A = RHS + ":[" + str1 + "]"
        elif str1 == "" :
            A = RHS + ":[" + str2 + "]"
        elif str1 != "" and str2 != "" :
            A = RHS + ":[" + str1 + " & " + str2 + "]"


# user has selected some dependent and/or some relation value(s)
        LHSdict = defaultdict(list)
        query = ""
        for item in v:
            LHSdict[item[0]].append((item[1], item[2]))
        # pprint(LHSdict)
        # print len(LHSdict.values())

        for key, value in LHSdict.items():
            str3 = ""
            str4 = ""
            str5 = ""
            for x in value:
                if x[0] == "rel":
                    str3 = "%s" %x[1]
                if x[0] == "dep":
                    str4 = "word=\"%s\"" %x[1]
                if x[0] == "dep_label":
                    str5 = "pos=\"%s\"" %x[1]
            if str4 == "" and str5 == "":
                B = ""
            elif str4 == "":
                B = "[" + str5 + "]"
            elif str5 == "":
                B = "[" + str4 + "]"
            elif str4 != "" and str5 != "":
                B = "[" + str4 + " & " + str5 + "]"

            C = str3
            if A != "" and B != "":
                x = A + " >" + str3 + " "+ B
            elif (A == "" or B == "") and C == "":
                x = A + B
            if C != "":
                if A == "" and B != "":
                    x = "#h%d >" %count + C + " " + B
                if B == "" and A != "":
                    x = A + " >" + C + " #d%d" %count
                if A == "" and B == "":
                    x = " #h%d >" %count + C + " #d%d" %count
            count += 1
            query += "(" + x + ")" + "\n&\n"

        # print query
        # print "------------"
        finalQuery += query
    index = finalQuery.rfind("\n&")
    #print finalQuery[:index]

# String modification: for dependents of the same head, only the variable of the head construction should be used
    tempQuery = finalQuery[:index]
    FQ = ""
    x = ""
    for line in tempQuery.splitlines():
        if line == "&":
            continue
        #line = line[1:-1]
        if ">" not in line:
            x = line[1:-1]
            #continue
        if ">" in line:
            if line[1:-1].split(">")[0] == x:
                y = line[1:-1].split(" >")[0]
                line = line.replace(y, x[0:3])
            else:
                x = line[1:-1].split(">")[0]
        FQ += line + "\n&"
    print "---------Query------------"
    print FQ[:-2]
    return FQ[:-2]


