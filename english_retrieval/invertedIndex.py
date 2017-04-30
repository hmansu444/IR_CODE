import os
import pickle
from bs4 import BeautifulSoup
from stemming.porter2 import stem as stem
import lxml
import gc

def readFiles(rootdir):
#rootdir = 'en.docs.2011'
	l=[]
	f=[]
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			#print os.path.join(subdir, file)
			l.append(os.path.join(subdir, file))
	for k in range(7):
		f.append(l[k*50000:(k+1)*50000])
	f.append(l[350000:])
	return f


def cleanText(text):
	b = "!,-=():;.?><\"\'\\%+\/#*"
	c = "\n\t"
	for char in b:
		text = text.replace(char,"")
	for char in c:
		text=text.replace(char," ")
	return text.split()


def removestopwords(words,stopWords):
	for word in words:
		if word in stopWords:
			words.remove(word)
	return words


def stemming(words):
	for word in words:
		word=stem(word)
	return words


def returnIndex(files):
	gc.collect
	posting={}
	count=0
	stopWords = [line.rstrip('\n') for line in open('stopwords.txt')]
	for file in files:
		try:
			docid=str(os.path.basename(file))
			#print (docid)
			words=[]
			count=count+1
			print(count)
			f = open(file, 'r')
			data = str(f.read())
			soup = BeautifulSoup(data, 'xml')
			title=""
			k=soup.findAll('TITLE')
			if k!=-1:
				title=str(soup.TITLE)
			tags = str(soup.TEXT)
			tags=tags+title
			contentWord = cleanText(tags)
			for word in words:
				word=word.lower()				
			words = contentWord	
			uniqueWords=list(set(words))
			uniqueWords=removestopwords(uniqueWords,stopWords)
			words=stemming(words)			
			uniqueWords=stemming(uniqueWords)	
			uniqueWords=list(set(uniqueWords))	

			for word in uniqueWords :	
				entry={docid:words.count(word)}
				
				if word in posting:
					posting[word].append(entry)
				else:
					posting[word]=[entry]
		except lxml.etree.XMLSyntaxError: 
				inc+=1
	return posting
		
if __name__=="__main__":
	rootdir="en.docs.2011"
	g=readFiles(rootdir)
	c=0
	for i in g:
		gc.collect()
		c+=1
		postingObject={}
		postingObject = returnIndex(i)
		
		with open('obj/'+str(c)+'.pkl', 'wb') as postingFile: 
			pickle.dump (postingObject, postingFile, pickle.HIGHEST_PROTOCOL)
		del postingObject
