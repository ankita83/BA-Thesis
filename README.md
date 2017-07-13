# BA-Thesis
BA Thesis (Treebank Querying, GrETEL)

run read_sentences.py: 
This script reads the the sentence entered by the user. 

/templates/index.html displays language options and the textbox to enter the sentence to the user. The entered sentence is then passed back to read_sentences.py to be processed further. 

generate_conll_format.py generates a list containg the conll format of the sentence entered by the user.
conll_to_standoff.py converts this list (conllu format of the senetence) to the standoff format(.ann format) used by bratnlp. 

bratObject.py converts the .ann object into two objects, namely the collection object and the document object, required in order to display the dependency tree. 

generate_options.py creates a list of [relation, head, head label, dependent, dependent label] for all relations in the selected sentence. 

The collection object, document object and the list of relations is finally passed to showSentence.xhtml, which displays the dependency tree and the relation options. 
