import lxml
from lxml import etree
import os
import glob
import pickle
import codecs
import time

#function for removing punctuation and all other special characters
def cleanText(text):
	b = "!,-।()॥:;.?><\"\'\\%+\/#*"
	for char in b:
		text = text.replace(char,"")
	return text.split()


#function for reding files and doing opertions in each and every file of given path
def readfiles(path):
	count = 0
	inc=0  #count of file in which parsing error is there
	posting={}#this will be the final posting object file initialized as Dictionary
	stopWords = [line.rstrip('\n') for line in open('stopWords.txt')]#getting stopwords from the file 'stopwords.txt'
	for infile in glob.glob( os.path.join(path, '*.txt') ):#this is to iterate in every file of the given path which can be given as a argument in the function
		try:
			l={}
			docid=str(infile)[-9:-4] #giving document id to each document for e.g. if(infile='hindi-document-00456.txt') --> docid= 00456
			words=[]
			count=count+1
			print(count)
			parsedfile= etree.parse(infile)    	#here i am doing xml parsing
			title = parsedfile.find('title').text     	# getting content of title tag
			content = parsedfile.find('content').text 	# getting content of content tag
			titleWord = cleanText(title) 		#removing Punctuations from title
			contentWord = cleanText(content)	#removing Punctuations from content
			words = titleWord + contentWord		# this is all the words in the file i.e. including the words in title as well as in content
			uniqueWords=list(set(words))		#geting uniqueWords out of those words
			uniqueWords=removestopwords(uniqueWords,stopWords)		#after getting uniqueWords, removing stopWords from those uniqueWords
			words=stemming(words)			#applying stemming over all the words
			uniqueWords=stemming(uniqueWords)	#applying stemming to all the uniquewords in next line
			uniqueWords=list(set(uniqueWords))	#after stemming we may get some similar terms,we need to take care of that too so, again taking uniquewords out of those words
  
			for word in uniqueWords :	#now iterating in uniqueWords 
				entry={docid:words.count(word)} #making a dictionary with given docid as key and count of word in file as value
				#now checking in our posting dictionary if that word exist or not
				#if exist	
				if word in posting: 
					posting[word].append(entry) # then we append our entry in the value of key 'word'
				else:
					posting[word]=[entry]  	#if doesn't exist then we make a key of that word and give value as our entry in the posting dictionary

		except lxml.etree.XMLSyntaxError: #checking for any error while parsing xml
			inc+=1
	return posting

#function for removing Stopwords it takes two arguments first one is list of words from which we have to remove Stopwords,and second list of stopwords
def removestopwords(words,stopWords):
	for word in words:
		if word in stopWords:
			words.remove(word)
	return words


# function for stemming which apply stemming over the words and returns the words after stemming has been done	
def stemming(words):
	suffixes = {
    1: ["ो","े","ू","ु","ी","ि","ा"],
    2: ["कर","ाओ","िए","ाई","ाए","ने","नी","ना","ते","ीं","ती","ता","ाँ","ां","ों","ें"],
    3: ["ाकर","ाइए","ाईं","ाया","ेगी","ेगा","ोगी","ोगे","ाने","ाना","ाते","ाती","ाता","तीं","ाओं","ाएं","ुओं","ुएं","ुआं"],
    4: ["ाएगी","ाएगा","ाओगी","ाओगे","एंगी","ेंगी","एंगे","ेंगे","ूंगी","ूंगा","ातीं","नाओं","नाएं","ताओं","ताएं","ियाँ","ियों","ियां"],
    5: ["ाएंगी","ाएंगे","ाऊंगी","ाऊंगा","ाइयाँ","ाइयों","ाइयां"],
}
	for i in range(0,len(words)):
            for L in 5, 4, 3, 2, 1:
                    if len(words[i]) > L + 1:
                            for suf in suffixes[L]:
                                    if words[i].endswith(suf):
                                            words[i]= words[i][:-L]
	return words

if __name__=="__main__":
	postingObject = readfiles('hindi')# calling readFiles function in the folder 'hindi' where we have all the documents
	with open('obj/abc.pkl', 'wb') as postingFile: #"""posting the obtained data in file post.pkl,  in obj folder """
        	pickle.dump (postingObject, postingFile, pickle.HIGHEST_PROTOCOL)
