# The sentence entered by the user is passed to this script.
# The sentence is passed as input to the SyntaxNet parser (parser.sh) which writes the conll format of the sentence into a file.
# The file is read and converted to a list that is returned to the main calling script.

import subprocess
import os
import tempfile
import config
import json
from pprint import pprint

outputFile = tempfile.NamedTemporaryFile(delete=False, dir=config.WORKING_DIRECTORY, suffix=".conllu")
language = ""

def getConllFormat(sentence):

    global language
    language = sentence[0]

    x = unicode(sentence[1])
    inputFile = tempfile.NamedTemporaryFile(delete=False, dir=config.WORKING_DIRECTORY, suffix=".txt")
    # outputFile = tempfile.NamedTemporaryFile(delete=False, dir=config.WORKING_DIRECTORY, suffix=".conllu")
    # print type(outputFile)

    inputFile.write(x.encode('utf-8'))
    inputFile.close()

    ip = os.path.basename(inputFile.name)
    op = os.path.basename(outputFile.name)

    # run bash commands from this script using subprocess
    command = '''
        MODEL_DIRECTORY="%s/%s"
        cat %s | %s $MODEL_DIRECTORY > %s
        ''' % (config.MODEL_DIRECTORY,sentence[0],ip, config.PARSER_PATH, op)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               cwd= config.WORKING_DIRECTORY)
    process.communicate(command)

    # read outputFile and write it to a list
    output = []
    for line in outputFile:
        output.append(line)

    outputFile.close()

    # delete all files created in the process
    os.remove(inputFile.name)
    # os.remove(outputFile.name)

    # return the list containing the conll format of the user enetered sentence
    return output


def getSelectedList(query):

    fq = "\"" + query.replace('"', '\\"') + "\""
    print fq

    # op = outputFile.name
    # print op
    # with open(op, 'r') as f:
    #     for line in f:
    #         print line

    # open(outputFile, 'r')
    command = '''
            CONLLU2_FILE=%s
            QUERY=%s
            LANGUAGE=%s
            API="https://weblicht.sfs.uni-tuebingen.de/tundra-beta/api/query/visres"
            curl -X POST -F "file=@$CONLLU2_FILE" -F "query=$QUERY" -F "lang=$LANGUAGE" "$API" > api-test.json
            ''' % (outputFile.name, fq, language)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process.communicate(command)

    with open("api-test.json") as dataFile:
        data = json.load(dataFile)
        selectedWord = []
        selectedRel = []
        nodes = set()
        relations = set()

        allNodes = {}
        allRels = {}

        for item in data:
            for x in item["d3Input"]["queryMatch"]:
                nodes.add(x["terminalPosition"])
            for y in item["d3Input"]["queryRelations"]:
                relations.add(y["id"])

        for item in data[0]["d3Input"]["nodes"]:
            key = item["node"].split("n")[1]
            value = item["name"]
            allNodes[key] = value
        for item in data[0]["d3Input"]["links"]:
            key = item["id"]
            value = item["dependency"]
            allRels[key] = value

        for k, v in allNodes.items():
            for x in nodes:
                if int(k) == x:
                    selectedWord.append(v)

        for k, v in allRels.items():
            for x in relations:
                if x == k:
                    selectedRel.append(v)
    # os.remove(outputFile.name)
    print selectedWord
    print selectedRel
    return [selectedWord, selectedRel, outputFile.name]
