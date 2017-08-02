# main script.
# user enters a sentence (index.html)
# selected sentence is then passed to the necessary scripts in order to finally view the dependency tree.
# and the tokens that the user can select in order to create a search query (in TIGERSearch format)

import web
from collections import defaultdict
import conll_to_standoff
import bratObject
import generate_options
from pprint import pprint
import generate_conll_format
import config
import string
import generate_query
import webbrowser as wb
import urllib as ul
import os
import sys

urls = ('/', 'index','/showSentence','showSentence','/displayOptions','displayOptions', '/displaySearch', 'displaySearch')
app = web.application(urls, globals())
web.config.debug = True
treebank = ""
bratObjects = []
# tempList = []
bratformat = []
finalQuery = ""
outputFile = ""
#----------------------- OLD CODE CAN BE DELETED ------------------------------
# output 10 random sentences from the UD English treebank
# The field "# text" contains the complete sentence

# file = open('/home/ankita/PycharmProjects/BAThesis/input_files/en-ud-dev.conllu', 'r')
# next(file)
# sentences = []
# conllSent = defaultdict(list)
# key = ""
# for line in file:
#     if "# sent_id" in line:
#         continue
#     if "# newdoc id" in line:
#         continue
#     if line not in ['\n', '\r\n']:
#         if "# text" in line:
#             temp = line.split("# text = ")[1]
#             key = temp.split("\n")[0]
#             sentences.append(key)
#             conllSent[key].append(None)
#         else:
#             conllSent[key].append(line)
#
# for k in conllSent.iterkeys():
#     del conllSent[k][0]

# Was included to debug. No need to generate a csv
# with open("temp.csv", 'w') as f:
#     writer = csv.writer(f)
#     for k,v in conllSent.iteritems():
#         writer.writerow([k] + v)

#random_list = random.sample(sentences, 10)
#-------------------------------------------------------------------------------

# Controller
class index:
    def __init__(self):
        self.render = web.template.render('templates/')

    def GET(self, name=None):
        return self.render.index(config.language_to_model)

class showSentence:
    def __init__(self):
        self.render = web.template.render('templates/')

    def POST(self):
        data = showSentence.get_sent(web.input().values())
        #pprint(data)
        return self.render.showSentence(data)

# process the sentence entered by the user: check punctuation errors, convert to conll format.
# Convert conll to standoff format for bratnlp.
# generate the necessary objects to view the dependency tree and the options that the user can select
    @classmethod
    def get_sent(self,sent):
        global treebank
        treebank = config.language_to_model[sent[0]]

        # check if there is a space before last punctuation character, if not insert one
        x = sent[1]
        if x[-1] in string.punctuation:
            if x[len(x)-1] != " ":
                temp = x[:-1] + " " + x[-1]
                sent[1] = temp

        conllOutput = generate_conll_format.getConllFormat(sent)
        # pprint(conllOutput)
        del conllOutput[-1]

        global bratformat
        bratformat = conll_to_standoff.process(conllOutput)
        options = generate_options.getLists(bratformat)

        # global tempList
        # del tempList[:]
        global bratObjects
        bratObjects = bratObject.createBratObjects(bratformat, [], [])
        return [bratObjects,options]

# Processes the options selected by the user to generate the search query
# and then view the search results
class displayOptions:
    def __init__(self):
        self.render = web.template.render('templates/')

    def POST(self):
        data = web.input()
        global finalQuery
        finalQuery = displayOptions.showOptions(data)

        tempList = generate_conll_format.getSelectedList(finalQuery)
        selectedWord = tempList[0]
        selectedRel = tempList[1]
        global outputFile
        outputFile = tempList[2]
        global bratObjects
        bratObjects = bratObject.createBratObjects(bratformat, selectedWord, selectedRel)

        return self.render.displayOptions(bratObjects,finalQuery)

    @classmethod
    def showOptions(self, options):
        finalQuery = generate_query.getQuery(options)
        return finalQuery

class displaySearch:
    def __init__(self):
        self.render = web.template.render('templates/')

    def POST(self):
        os.remove(outputFile)
        q = ul.quote(finalQuery.encode('utf-8'))
        wb.open("https://weblicht.sfs.uni-tuebingen.de/tundra-beta/public/treebank.html?bank=%s&q=%s" % (treebank, q))
        return None

if __name__ ==\
        '__main__':
    app.run()

#--------------------------------------------------------