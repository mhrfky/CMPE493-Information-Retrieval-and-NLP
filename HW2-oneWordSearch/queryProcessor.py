# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:44:44 2020

@author: mhrfk
"""
from trie import trie
import json
import pickle
import sys


def getTrie(): #gets the trie from already existed pickle file
    with open('trie.pickle', 'rb') as triepickle:
        y = pickle.load(triepickle)
        triepickle.close()
    return y

def getList():  #gets the inverted index dictionary from a already existant file
    y = {}
    with open('invertedindex.json', 'r') as listjson:
        y = json.load(listjson)
        listjson.close()
    return y
def getIndexes(words: []):  #gets the ids of the articles that at least one of the words is in
    result = []
    for word in words:
        result += invertedlist[word]
    return list(set(result))
trie = getTrie()
invertedlist = getList()

words = trie.get(sys.argv[1].lower())

indexes = getIndexes(words)
indexes.sort()
print(indexes)
resultfile = open("result.txt",'a+')
resultfile.write(str(sys.argv[1] + "\n"))
resultfile.write(str(indexes))