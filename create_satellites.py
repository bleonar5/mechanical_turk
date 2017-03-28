
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.probability import *
import nltk
from heapq import heappush, heappop

import csv

antonyms = {}
attributes = {}
checkded_adjs = {}
for synset in list(wn.all_synsets()):
    if synset.pos() == 'a' or synset.pos() == 's':
        if len(synset.attributes()) > 0:
            if synset.attributes()[0] not in attributes:
                if len(synset.similar_tos()) > 0:
                    ex0 = synset.similar_tos()
                    ex0.append(synset)
                else:
                    ex0 = [synset]
                attributes[synset.attributes()[0]] = ex0
            else:
                if len(synset.similar_tos()) > 0:
                    ex = synset.similar_tos()
                    ex.append(synset)
                    attributes[synset.attributes()[0]].extend(ex) 
                else:
                    attributes[synset.attributes()[0]].append(synset) 
        
# .name is good key to lookup things, test it
#for atr in attributes:
 #   print('Atr', atr.name())
  #  print(a.lemmas_names()[0] for a in attributes[atr])

print("next step")

from nltk.stem.lancaster import LancasterStemmer

words = FreqDist([w.lower() for w in brown.words()])

st = LancasterStemmer()

heap = []

dic = {}

#for sentence in brown.sents():
#	for word in sentence:
#		words.inc(word.lower())


with open('stimuli.csv','w') as f:
	writer = csv.writer(f)

	for atr in attributes:
		dic = {}
		li = [atr.lemmas()[0].name(),atr.lemmas()[0].key().split('%')[0] + '_' + atr.lemmas()[0].key().split('%')[1] +'_'+ atr.definition()]
		heap = []

		top_freqs = set()
		for syn in attributes[atr]:
			lems = []
			for lem in syn.lemmas():
				heappush(lems,(1-words.freq(lem.name()),lem))
			lem = heappop(lems)[1]
			stem = st.stem(lem.name())
			if stem not in dic:
				dic[stem] = [(1-words.freq(lem.name()),lem,syn.definition())]
			else:
				heappush(dic[stem], (1-words.freq(lem.name()),lem, syn.definition()))

		for key in dic.keys():
			heappush(heap, heappop(dic[key]))

		for x in range(0,20):
			
			if len(heap) > 0:
				popped = heappop(heap)
				li.append(popped[1].name() + '/' + popped[1].key() + '/' + popped[2])
			else:
				break

		print atr.name() + ' : ' + str(li)





		if len(li) >= 5:
			writer.writerow(li)
