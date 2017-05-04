# BA-Thesis
BA Thesis (Treebank Querying, GrETEL)

run read_sentences.py: 
This script reads the conllu file and randomly selects 10 sentences. 

/templates/index.html displays these 10 sentences to the user. The selected sentence is then passed back to read_sentences.py to be processed further. 

conll_to_standoff.py converts the selected sentence (conllu format) to teh standoff format(.ann format) used by bratnlp. 

bratObject.py converts the .ann object into two objects, namely the collection object and the document object, required in order to display the dependency tree. 

generate_options.py creates a list of [relation, head, head label, dependent, dependent label] for all relations in teh selected sentence. 

The collection object, document object and the list of relations is finally passed to showSentence.xhtml, which displays the dependency tree and the relation options. 
