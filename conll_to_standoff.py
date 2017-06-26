# Convert a sentence in conllU format to the standoff format required by brat nlp.

import sys
from pprint import pprint

# whether to output an explicit root note
OUTPUT_ROOT = True
# the string to use to represent the root node
ROOT_STR = 'ROOT'

# rewrites for characters appearing in CoNLL-X types that cannot be
# directly used in identifiers in brat-flavored standoff
charmap = {
    '<' : '_lt_',
    '>' : '_gt_',
    '+' : '_plus_',
    '?' : '_question_',
    '&' : '_amp_',
    ':' : '_colon_',
    '.' : '_period_',
    '!' : '_exclamation_',
}

def maptype(s):
    return "".join([charmap.get(c,c) for c in s])

def tokstr(start, end, ttype, idnum, text):
    return "T%d\t%s %d %d\t%s" % (idnum, maptype(ttype), start, end, text)

def depstr(depid, headid, rel, idnum):
    return "R%d\t%s Arg1:T%d Arg2:T%d" % (idnum, maptype(rel), headid, depid)

def process(sentence):
    tokens, deps = [], []

    for l in sentence:
        #print l
        if l is not None:
            fields = l.split('\t')
        else:
            print "Something went wrong in the list"
            sys.exit(0)
        ID, form, POS = fields[0], fields[1], fields[3]
        head, rel = fields[6], fields[7]

        tokens.append((ID, form, POS))
        # allow value "_" for HEAD to indicate no dependency
        if head != "_":
            deps.append((ID, head, rel))
    return output(tokens,deps)

def output(tokens, deps):
    annout = []
    offset, idnum, ridnum = 0, 1, 1
    #doctext = ""

    # store mapping from per-sentence token sequence IDs to
    # document-unique token IDs
    idmap = {}

    # output tokens
    prev_form = None

    if OUTPUT_ROOT:
        # add an explicit root node with seq ID 0 (zero)
        tokens = [('0', ROOT_STR, ROOT_STR)] + tokens

    for ID, form, POS in tokens:

        if prev_form is not None:
            #doctext = doctext + ' '
            offset += 1

        # output a token annotation
        annout.append(tokstr(offset, offset + len(form), POS, idnum, form))
        idmap[ID] = idnum
        idnum += 1

        #doctext = doctext + form
        offset += len(form)

        prev_form = form

    # output dependencies
    for dep, head, rel in deps:

        # if root is not added, skip deps to the root (idx 0)
        if not OUTPUT_ROOT and head == '0':
            continue

        annout.append(depstr(idmap[dep], idmap[head], rel, ridnum))
        ridnum += 1

    #doctext = doctext + '\n'
    offset += 1
    #pprint(annout)
    return annout