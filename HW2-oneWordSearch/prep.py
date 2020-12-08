# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 01:11:28 2020

@author: mhrfk
"""
import json
import re
import os
import pickle
from trie import trie
import string
inversedict = {}
def getstopWords(): # reads and splits the stopwords
    sf = open("stopwords.txt",'r')
    return sf.read().split()
    
def getWords(text : str): 
    
    title = getTitle(text) #gets the title
    body = getBody(text)    #gets the body part of the current article
    aid = getID(text)       #gets the id of the current article
    wordlist = []
    if title != -1:         #checks if title exists and add the words to the list
        wordlist = wordlist + title.lower().split() 
    if body != -1:          #checks if body exists and add the words to the list
        wordlist = wordlist + body.lower().split()
    wordlist = list(set(wordlist))        #removes the duplicates
    stopwords = getstopWords()              
    for stop in stopwords:                  #removes the stopwords
        try:
            wordlist.remove(stop)
        except:
            pass
    makeinversedict(wordlist,int(aid))      #and add the words to the inversedict with the current article id
    #print(wordlist)
def makeinversedict(wordlist : list,articleId: int):
    for word in wordlist:
        if word in inversedict:         #appends the id if word exists in dictionary
            inversedict[word].append(articleId)        
        else:                           #adds the word with the id if it doesn't exists in dictionary
            inversedict[word] = [articleId]
def getID(text : str):                  
    start = text.find("NEWID=") + 7
    end = start
    while True:
        if text[end] == '"':
            break
        end += 1
    
    return text[start:end]


def getTitle(text : str):
    start = text.find("<TITLE>") + 7
    if start == 6:
        return -1
    end = text.find("</TITLE>")
    #print(text[start:end])
    return replaceAndCaseFolding(text[start:end])
def getBody(text : str):
    start = text.find("<BODY>") + 6
    if start == 5:
        return -1
    end = text.find("</BODY>")
    return replaceAndCaseFolding(text[start:end])

def replaceAndCaseFolding(text : str): #removes punctuations
    text = text.replace('\t', ' ')
    text = text.replace('\n', ' ')
    
    for c in string.punctuation:
        if c != "'":
            text = text.replace(c, ' ')
        else:
            text = text.replace("'s", "")
    
    return text
all_files = os.listdir("reuters21578/")

for f in all_files:     #read all the files with .sgm extension
    if f[-4:] == ".sgm":
        fi = open("reuters21578/" + f,mode = 'r', encoding = 'latin-1')
        text = fi.read()
        # print(f)

        while True:
            start = text.find("<REUTERS")
            end = text.find("</REUTERS>")
            #print(text[start:end])
            
            if start == -1:
                break
            getWords(text[start:end])
            text = text[end+11:]
                
        

tr = trie()             #creates a trie object and adds the every word recorded in the files
for word in inversedict:
    tr.add(word)
    
triefile = open("trie.pickle",'wb') #pickle the trie object for later use
pickle.dump(tr, triefile)
triefile.close()

with open('invertedindex.json', 'w') as outfile: #json the invertedindex dictionary for later use
    json.dump(inversedict, outfile)

















