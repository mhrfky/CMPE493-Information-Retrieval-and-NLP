import math
import json
import string
import os
import re

"""
referenced from : https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
get a text string and removes the html code which provide no readeble content
@params:
    raw_html: string
@return
    a clean string, in which the unnecessary html codes have been removed
"""
def cleanhtml(raw_html : str):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
"""
get a text string and removes the unnecessary postfixes
@params:
    desc: string
@return
    a clean string, in which the unnecessary postfixes have been removed
"""
def punctRemoval(desc : str):

    desc= desc.replace("'s", "")
    desc= desc.replace("'m", "")
    desc= desc.replace("'re", "")
    desc= desc.replace("'d", "")
    

    return cleanhtml(desc)

"""
get a text string and tokenize with the seperator as ' '
@params:
    desc: string
@return
    a list of tokenized words
"""
def tokenization(desc : str):
    return desc.lower().split()
"""
get a tokens list and removes the punctiotiond
@params:
    tokens: list
@return
    a list of tokenized words
"""
def punctuationRemoval(tokens:list):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    tokens = [token.translate(translator) for token in tokens]  # Punctuation Removal
    str_tokens = " ".join(token for token in tokens)  # Retokenize the tokens that include any whitespaces after punctuation removal.
    tokens = str_tokens.split()
    return tokens

"""
get a string and normalize the content, and return a tokens list
@params:
    desc: string
@return
    a list of tokenized words
"""
def normalization(desc : str):
    a = punctRemoval(desc)
    b = tokenization(a)
    a = punctuationRemoval(b)
    return a
"""
@return
     the dictionary of object-like dictionaries about the content of the book which has been stored in json format
"""
def getBooks():        
    books = {}
    f = open("booksOut.json",'r')
    y = f.read()
    f.close()
    return json.loads(y)
"""
@return
     a dictionary which holds the words as key to a dictionary of urls as key and tf values as values.
"""
def getInverted():
    inverted = {}
    for url in books:
        words = normalization(books[url]["desc"])
        for word in words:
            if word not in inverted:
                inverted[word] = {}
                inverted[word][url] = 1
            else:
                if url not in inverted[word]:
                    inverted[word][url] = 1
                else:
                    inverted[word][url]+= 1
                    
        for word in inverted:
            if url in inverted[word]:
                freq = inverted[word][url]  
                inverted[word][url]  = 1 + math.log10(freq)
    return inverted

"""
@return
     tfidf:xa dictionary which holds the words as key to a dictionary of urls as key and tfidf values as values.
     idf:a dictionary which holds the words as key to a dictionary of urls as key and idf values as values.
     lengthOftheDoc:a dictionary which holds the urls as key to the length of the tfidfs in it.

"""
def getTFIDF():
    inverted = getInverted()
    lengthOftheDoc = {}
    for url in books:
        lengthOftheDoc[url] =0
    
    tfidfs = {}
    idfs = {}
    for word in inverted:
        numberForIDF = len(inverted[word])                 #number of the documents word is in
        tfidfs[word] = {}
        idfs[word] = math.log10(numberOfbooks/numberForIDF)                 #idf value for the word
        for doc in inverted[word]:
            tfidfs[word][doc] = inverted[word][doc] * idfs[word] #tfidf value for the word in that doc
            lengthOftheDoc[doc] += tfidfs[word][doc] * tfidfs[word][doc]
            
    for doc in lengthOftheDoc:
        lengthOftheDoc[doc] = math.sqrt(lengthOftheDoc[doc])
    return (tfidfs,idfs,lengthOftheDoc)

"""
In genre, the same modelling in the description has been used(tfidf). For tf
how many people chose the genre to be has been considered.
@return
     tfidf:xa dictionary which holds the genres as key to a dictionary of urls as key and tfidf values as values.
     idf:a dictionary which holds the genres as key to a dictionary of urls as key and idf values as values.
     lengthOftheDoc:a dictionary which holds the urls as key to the length of the tfidfs in it.

"""
def getGenres():
    genreInversed = {}
    for book in books:
        for genre in books[book]["genres"]:
            if genre in genreInversed:
                genreInversed[genre][book] =  int(books[book]["genres"][genre])
            else:
                genreInversed[genre] = {}
                genreInversed[genre][book] = int(books[book]["genres"][genre])
                
    lengthOftheDoc = {}
    for url in books:
        lengthOftheDoc[url] =0
    tfidfs = {}
    idfs = {}
    for genre in genreInversed:
        numberForIDF = len(genreInversed[genre])                 #number of the documents word is in
        tfidfs[genre] = {}
        idfs[genre] = math.log10(numberOfbooks/numberForIDF)                 #idf value for the word
        for doc in genreInversed[genre]:
            tfidfs[genre][doc] = genreInversed[genre][doc] * idfs[genre] #tfidf value for the word in that doc
            lengthOftheDoc[doc] += tfidfs[genre][doc] * tfidfs[genre][doc]
            
    for doc in lengthOftheDoc:
        lengthOftheDoc[doc] = math.sqrt(lengthOftheDoc[doc])
    return (tfidfs,idfs,lengthOftheDoc)

books= {}
#for words
tfidfs= {}
idfs= {}
lengthOftheDoc = {}
#for genres
gtfidfs= {}
gidfs= {}
glengthOftheDoc = {}

numberOfbooks = 0
"""
Check if one of them is missing. If so the process of creating them is started.
If they exists, the next step,query processing is started.
"""
if not os.path.exists(os.path.join(os.getcwd(),'tfidfs.json')) or\
    not os.path.exists(os.path.join(os.getcwd(),'idfs.json')) or\
    not os.path.exists(os.path.join(os.getcwd(),'lengthOftheDoc.json')) or\
    not os.path.exists(os.path.join(os.getcwd(),'gtfidfs.json')) or\
    not os.path.exists(os.path.join(os.getcwd(),'gidfs.json')) or\
    not os.path.exists(os.path.join(os.getcwd(),'glengthOftheDoc.json')):
        
    books = getBooks()
    urlsToBeDeleted = []
    for url in books:
        if books[url]["recomms"] == []:
            urlsToBeDeleted.append(url)
    for url in urlsToBeDeleted:
        del books[url]

    numberOfbooks = len(books)
    
    
    tfidfs,idfs,lengthOftheDoc = getTFIDF()
    
    f = open("tfidfs.json",'w')
    f.write(json.dumps(tfidfs))
    f.close()
    f = open("idfs.json",'w')
    f.write(json.dumps(idfs))
    f.close()
    f = open("lengthOftheDoc.json",'w')
    f.write(json.dumps(lengthOftheDoc))
    f.close()
    del tfidfs,idfs,lengthOftheDoc

    
    gtfidfs,gidfs,glengthOftheDoc = getGenres()

    f = open("gtfidfs.json",'w')
    f.write(json.dumps(gtfidfs))
    f.close()
    f = open("gidfs.json",'w')
    f.write(json.dumps(gidfs))
    f.close()
    f = open("glengthOftheDoc.json",'w')
    f.write(json.dumps(glengthOftheDoc))
    f.close()
    del gtfidfs,gidfs,glengthOftheDoc,books
    


    