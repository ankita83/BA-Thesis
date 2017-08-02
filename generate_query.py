# Method to generate the TIGER Search query from the options selected by the user

from collections import defaultdict
from pprint import pprint
import tigerAST as ast

def getQuery(data):
    queryItems = defaultdict(list)

    queryItems1 = defaultdict(dict)

    for k,v in data.items():
        temp = k.split(":")
        key = temp[0]
        x = temp[1].split(" ")
        queryItems[key].append((x[0], x[1], v))

    for key,value in queryItems.items():
        reldict = defaultdict(list)
        for v in value:
            reldict[v[0]].append((v[1], v[2]))

        queryItems1[key] = reldict

    pprint(queryItems1)

# structure - dict1(dict2(list of tuples))
# eg: {'T3': { 'rel-0': [('rel', u'det'), ('dep', u'The'), ('head_label', u'NOUN')] } }

    FQ = []
    for key1, dict2 in queryItems1.items():
        token = key1
        root = []
        A = ""
        B = ""
        for key2, value2 in dict2.items():
            variable = key2.split("-")[1]
            C = ""
            D = ""
            rel = None
            for item in value2:
                if item[0] == "head":
                    A = ast.AttributeValue("word", item[1])
                if item[0] == "head_label":
                    B = ast.AttributeValue("pos", item[1])
                if item[0] == "dep":
                    C = ast.AttributeValue("word", item[1])
                if item[0] == "dep_label":
                    D = ast.AttributeValue("pos", item[1])
                if item[0] == "rel":
                    rel = item[1]

            if A!="" or B!="":
                head = ast.Token(token, ast.Conjunction([A,B]))
            else:
                if rel != None:
                    head = ast.Token(token)
                else:
                    head = None
            if C!="" or D!="":
                dep = ast.Token("d"+variable, ast.Conjunction([C,D]))
            else:
                if rel != None:
                    dep = ast.Token("d"+variable)
                else:
                    dep = None
            # To avoid repeating the head values when referencing the head again and just using the token reference
            if len(root) >= 1 and head != None:
                head = ast.Token(token)
            Y = ast.DepRel(head, dep, rel)
            root.append(Y)

            # for k,v in Y.__dict__.items():
            #     print k
            #     print v.__class__.__name__
        if len(root) >= 2:
            Y1 = root[0]
            Y2 = root[1]
            if (root[0].__dict__["_rel"] == None) and (root[0].__dict__["_dep"] == None):
                root[1].__dict__["_head"] = root[0].__dict__["_head"]
                del root[0]

        #print Y.__class__.__name__

        FQ.append(ast.Conjunction(root))
    print "----- AST Query ---------------------------"
    print ast.Conjunction(FQ)
    print "-------------------------------------------"
    h = ast.Conjunction(FQ)
    return str(h)

'''
# ----------------- Before AST code , can be deleted if AST code works fine --------------------------------------
    # A: Head part, C: relation part, B: Dependent part
    for k,v in data.items():
        temp = k.split(":")
        key = temp[0]
        x = temp[1].split(" ")
        queryItems[key].append((x[0], x[1], v))

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

'''
