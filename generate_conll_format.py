# The sentence entered by the user is passed to this script.
# The sentence is passed as input to the SyntaxNet parser (demo.sh) which writes the conll format of the sentence into a file.
# The file is read and converted to a list that is returned to the main calling script.

import subprocess
import os

# main method that calls the respective methods depending on the language selected
# in order to generate the conll format.
def getConllFormat(sentence):
    if sentence[0] == "en":
        output = enConllFormat(sentence[1])
    elif sentence[0] == "de":
        output = deConllFormat(sentence[1])
    elif sentence[0] == "es":
        output = esConllFormat(sentence[1])
    else:
        print "No correct language selected"
    return output

# ENGLISH
def enConllFormat(sentence):
    #write sentence to a file sentences_en.txt
    inputFile = open('/home/ankita/models/syntaxnet/sentences_en.txt', 'w')
    inputFile.write(sentence)
    inputFile.close()

    # run bash commands from this script using subprocess
    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/english"
    bazel build syntaxnet:parser_eval
    cat sentences_en.txt | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > output_en.conll
    '''
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    #read output_en.conll file and write it to a list
    outputFile = open('/home/ankita/models/syntaxnet/output_en.conll', 'r')
    output_en = []
    for line in outputFile:
        output_en.append(line)
    outputFile.close()

    #delete all files created in the process
    os.remove('/home/ankita/models/syntaxnet/sentences_en.txt')
    os.remove('/home/ankita/models/syntaxnet/output_en.conll')

    #return the list containing the conll format of the user enetered sentence
    return output_en

# GERMAN
def deConllFormat(sentence):
    # write sentence to a file sentences_en.txt
    inputFile = open('/home/ankita/models/syntaxnet/sentences_de.txt', 'w')
    inputFile.write(sentence)
    inputFile.close()

    # run bash commands from this script using subprocess
    command = '''
    MODEL_DIRECTORY="/home/ankita/models/syntaxnet/syntaxnet/models/german"
    bazel build syntaxnet:parser_eval
    cat sentences_de.txt | syntaxnet/models/parsey_universal/parse.sh $MODEL_DIRECTORY > output_de.conll
    '''
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                               cwd='/home/ankita/models/syntaxnet/')
    process.communicate(command)

    # read output_en.conll file and write it to a list
    outputFile = open('/home/ankita/models/syntaxnet/output_de.conll', 'r')
    output_de = []
    for line in outputFile:
        output_de.append(line)
    outputFile.close()

    # delete all files created in the process
    os.remove('/home/ankita/models/syntaxnet/sentences_de.txt')
    os.remove('/home/ankita/models/syntaxnet/output_de.conll')

    # return the list containing the conll format of the user enetered sentence
    return output_de

# SPANISH
def esConllFormat(sentence):
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