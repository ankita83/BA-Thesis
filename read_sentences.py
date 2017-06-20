# main script.
# randomly selects 10 sentences to be displayed to the user
# selected sentence is then passed to the necessary scripts in order to finally view the dependency tree.

import random
import web
from collections import defaultdict
import csv
import conll_to_standoff
import bratObject
import generate_options
import generate_query
from pprint import pprint
import generate_conll_format


urls = ('/', 'index','/showSentence','showSentence','/displayOptions','displayOptions')
app = web.application(urls, globals())
web.config.debug = True

# output 10 random sentences from the UD English treebank
# The field "# text" contains the complete sentence

file = open('/home/ankita/PycharmProjects/BAThesis/input_files/en-ud-dev.conllu', 'r')
next(file)
sentences = []
conllSent = defaultdict(list)
key = ""
for line in file:
    if "# sent_id" in line:
        continue
    if "# newdoc id" in line:
        continue
    if line not in ['\n', '\r\n']:
        if "# text" in line:
            temp = line.split("# text = ")[1]
            key = temp.split("\n")[0]
            sentences.append(key)
            conllSent[key].append(None)
        else:
            conllSent[key].append(line)

for k in conllSent.iterkeys():
    del conllSent[k][0]

# Was included to debug. No need to generate a csv
# with open("temp.csv", 'w') as f:
#     writer = csv.writer(f)
#     for k,v in conllSent.iteritems():
#         writer.writerow([k] + v)

random_list = random.sample(sentences, 10)

# Controller
class index:
    def __init__(self):
        self.render = web.template.render('templates/')

    def GET(self, name=None):
        return self.render.index(random_list)

class showSentence:
    def __init__(self):
        self.render = web.template.render('templates/')

    def POST(self):
        data = showSentence.get_sent(web.input().values())
        return self.render.showSentence(data)

    @classmethod
    # def get_sent(self,sent):
    #     bratformat = []
    #     x = sent[0]
    #     for k in conllSent.iterkeys():
    #         key = k.decode('utf-8')
    #         if x == key:
    #             pprint(conllSent.get(key))
    #             bratformat = conll_to_standoff.process(conllSent.get(key))
    #             break

    def get_sent(self,sent):
        print sent[0]
        print sent[1]
        conllOutput = generate_conll_format.getConllFormat(sent)
        del conllOutput[-1]
        bratformat = conll_to_standoff.process(conllOutput)


        options = generate_options.getLists(bratformat)
        bratObjects = bratObject.createBratObjects(bratformat)
        return [bratObjects,options]

class displayOptions:
    def __init__(self):
        self.render = web.template.render('templates/')

    def POST(self):
        data = web.input()
        displayOptions.showOptions(data)
        return None

    @classmethod
    def showOptions(self, options):
        #generate_query.getQuery1(options)
        finalQuery = generate_query.getQuery(options)
        print finalQuery
        # for k, v in options.items():
        #     print k, v


if __name__ ==\
        '__main__':
    app.run()

#--------------------------------------------------------