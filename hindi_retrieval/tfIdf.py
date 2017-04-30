import pickle
import math
import operator
import invIndex
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
				
if __name__=="__main__":
	with open('obj/post.pkl', 'rb') as f:
		data= pickle.load(f)
	#print(len(data))
	w={}
	stopWords = [line.rstrip('\n') for line in open('stopWords.txt')]
	query=input("enter query")
	query=invIndex.cleanText(query)
	#print(query)
	query=invIndex.stemming(query)
	for i in query:	
		query=str(i)
	k=data[query]
	print(k)
	i='00044' 
	if i in k:
		print("True")
	else:
		print("False")
	query=list(set(invIndex.removestopwords(query,stopWords)))
	
	for word in query:	
		j,b=termfrequency(word,data)
		for i in j.keys():
			if i not in w:
				w[i]=j[i]*math.log(50633/b,10)
			else:
				k=w[i]+j[i]*math.log(50633/b,10)
				l={i:k}					
				w.update(l)

	sorted_w = sorted(w.items(), key=operator.itemgetter(1))
	for k in sorted_w:
		print(k[0]+"\t\t"+str(k[1])+"\n")
	#print(math.log(50633/b,10))
	#print(b)
	#print(numberOfWordsInDicument('00003',data))
	#print(len(w))
	#print(c)
