# The sentence entered by the user is passed to this script.
# The sentence is passed as input to the SyntaxNet parser (parser.sh) which writes the conll format of the sentence into a file.
# The file is read and converted to a list that is returned to the main calling script.

import subprocess
import os
import tempfile
import config


def getConllFormat(sentence):

    x = unicode(sentence[1])
    inputFile = tempfile.NamedTemporaryFile(delete=False, dir=config.WORKING_DIRECTORY, suffix=".txt")
    outputFile = tempfile.NamedTemporaryFile(delete=False, dir=config.WORKING_DIRECTORY, suffix=".conll")

    inputFile.write(x.encode('utf-8'))
    inputFile.close()

    ip = os.path.basename(inputFile.name)
    op = os.path.basename(outputFile.name)
    # run bash commands from this script using subprocess

    command = '''
        MODEL_DIRECTORY="%s/%s"
        cat %s | %s $MODEL_DIRECTORY > %s
        ''' % (config.MODEL_DIRECTORY,sentence[0],ip, config.PARSER_PATH, op)
    #print command
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
    os.remove(outputFile.name)

    # return the list containing the conll format of the user enetered sentence
    return output


#--------------------------------- OLD CODE CAN BE DELETED ---------------------------------------------------------

# Rest of the code and the functions can be deleted

    # if sentence[0] == "en":
    #    output = enConllFormat(inputFile, outputFile, sentence[1])
    #
    # elif sentence[0] == "de":
    #     output = deConllFormat(inputFile, outputFile, sentence[1])
    # elif sentence[0] == "es":
    #     output = esConllFormat(inputFile, outputFile, sentence[1])
    # elif sentence[0] == "du":
    #     output = duConllFormat(inputFile, outputFile, sentence[1])
    # else:
    #     print "No correct language selected"
    # return output

# ENGLISH
def enConllFormat(inputFile, outputFile, sentence):

    inputFile.write(sentence)
    inputFile.close()

    ip = os.path.basename(inputFile.name)
    op = os.path.basename(outputFile.name)
    # run bash commands from this script using subprocess

    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/english"
    cat %s | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > %s
    ''' %(ip,op)
    print command
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    #read outputFile and write it to a list
    output_en = []
    for line in outputFile:
        output_en.append(line)
    outputFile.close()

    #delete all files created in the process
    os.remove(inputFile.name)
    os.remove(outputFile.name)

    #return the list containing the conll format of the user enetered sentence
    return output_en

# GERMAN
def deConllFormat(inputFile, outputFile, sentence):

    inputFile.write(sentence)
    inputFile.close()

    ip = os.path.basename(inputFile.name)
    op = os.path.basename(outputFile.name)

    # run bash commands from this script using subprocess
    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/german"
    cat %s | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > %s
    ''' %(ip,op)
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    # read output_en.conll file and write it to a list
    output_de = []
    for line in outputFile:
        output_de.append(line)
    outputFile.close()

    # delete all files created in the process
    os.remove(inputFile.name)
    os.remove(outputFile.name)

    # return the list containing the conll format of the user enetered sentence
    return output_de

# SPANISH
def esConllFormat(inputFile, outputFile, sentence):
    #write sentence to a file sentences_en.txt
    inputFile = open('/home/ankita/models/syntaxnet/sentences_es.txt', 'w')
    inputFile.write(sentence)
    inputFile.close()

    # run bash commands from this script using subprocess
    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/spanish"
    bazel build syntaxnet:parser_eval
    cat sentences_es.txt | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > output_es.conll
    '''
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    #read output_en.conll file and write it to a list
    outputFile = open('/home/ankita/models/syntaxnet/output_es.conll', 'r')
    output_es = []
    for line in outputFile:
        output_es.append(line)
    outputFile.close()

    #delete all files created in the process
    os.remove('/home/ankita/models/syntaxnet/sentences_es.txt')
    os.remove('/home/ankita/models/syntaxnet/output_es.conll')

    #return the list containing the conll format of the user enetered sentence
    return output_es

# DUTCH
def duConllFormat(inputFile, outputFile, sentence):
    #write sentence to a file sentences_en.txt
    inputFile = open('/home/ankita/models/syntaxnet/sentences_du.txt', 'w')
    inputFile.write(sentence)
    inputFile.close()

    # run bash commands from this script using subprocess
    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/dutch"

    cat sentences_du.txt | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > output_du.conll
    '''
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    #read output_en.conll file and write it to a list
    outputFile = open('/home/ankita/models/syntaxnet/output_du.conll', 'r')
    output_du = []
    for line in outputFile:
        output_du.append(line)
    outputFile.close()

    #delete all files created in the process
    os.remove('/home/ankita/models/syntaxnet/sentences_du.txt')
    os.remove('/home/ankita/models/syntaxnet/output_du.conll')

    #return the list containing the conll format of the user enetered sentence
    return output_du