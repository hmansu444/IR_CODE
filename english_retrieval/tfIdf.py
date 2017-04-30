import pickle
import math
import operator
import invertedIndex
import os
from collections import OrderedDict

def termfrequency(word,diction):
	if word in diction :
		k=diction[word]
		tf={}
		for i in k:
			tf.update(i)
		return tf,len(k)
def numberOfWordsInDocument(docid,diction):
	count=0
	for i in diction:
		j=diction[i]
		for k in j:
			if docid in k:
				count+=k[docid]
	return count

def queryOptimize(query):
	stopWords = [line.rstrip('\n') for line in open('stopwords.txt')]
	query=invertedIndex.cleanText(query)
	#print(query)
	query=list(set(invertedIndex.removestopwords(query,stopWords)))
	#print(query)
	query=invertedIndex.stemming(query)
	query=list(set(query))
	return query

def dataLoad(filePath):
	with open(filePath, 'rb') as f:
		data= pickle.load(f)
	return data			
if __name__=="__main__":
	query=input("enter query")
	query=queryOptimize(query)
	w={}
	d = OrderedDict()
	directory="obj/"
	for filename in os.listdir(directory):
		if filename.endswith(".pkl") :
			data= dataLoad("obj/"+str(filename))
			#title= dataLoad('obj/title.pkl')	
			for word in query:	
				j,b=termfrequency(word,data)
				for i in j.keys():
					tf=j[i]
					if i not in w:
						w[i]=tf*math.log(50000/b,10)
					else:
						k=w[i]+ (tf*math.log(50000/b,10))
						l={i:k}					
						w.update(l)
			del data
			print ("successful")
			
	sorted_w = sorted(w.items(), key=operator.itemgetter(1))
	print (len(sorted_w))
	for k in sorted_w:
		d[k[0]]=str(k[1])
	#els = list(d.items())
	for key in d:
		print(key+"\t\t"+str(d[key])+"\n")
			
