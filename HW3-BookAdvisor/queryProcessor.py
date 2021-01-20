import os
import pathlib
import reader,tfidf
import math
import json
import sys


def getQtfidf(queryData : dict):
    tokens = tfidf.normalization(queryData["desc"])
    tfidfs = {}
    for token in tokens:
        if token in tfidfs:
            tfidfs[token] += 1
        else:
            tfidfs[token] = 1
    qLength = 0
    for word in tfidfs:
        tfidfs[word] = (1 + math.log10(tfidfs[word])) * idfs[word]
        qLength += tfidfs[word]*tfidfs[word]
    qlength = math.sqrt(qLength)
    return tfidfs,qlength

def getQgtfidf(queryData : dict):
    genreLength = 0
    genres = {}
    for genre in queryData["genres"]:
        if genre in gtfidfs and genre in gidfs:

            genres[genre] = (1 + math.log10(int(queryData["genres"][genre]))) * gidfs[genre]
            genreLength += genres[genre]*genres[genre]
    genreLength = math.sqrt(genreLength)
    return genres,genreLength


if 'https://' in sys.argv[1]:
    
        
    
    f = open("tfidfs.json",'r')
    y = f.read()
    f.close()
    tfidfs = json.loads(y)
    
    f = open("idfs.json",'r')
    y = f.read()
    f.close()
    idfs = json.loads(y)
    
    f = open("lengthOftheDoc.json",'r')
    y = f.read()
    f.close()
    lengthOftheDoc = json.loads(y)
    
    f = open("gtfidfs.json",'r')
    y = f.read()
    f.close()
    gtfidfs = json.loads(y)
    
    f = open("gidfs.json",'r')
    y = f.read()
    f.close()
    gidfs = json.loads(y)
    
    f = open("glengthOftheDoc.json",'r')
    y = f.read()
    f.close()
    glengthOftheDoc = json.loads(y)
    
    queryData = reader.getData(sys.argv[1])
    
    products = {}
    gproducts = {}
        
        
    
    
    qtfidfs,qlength = getQtfidf(queryData)
    qgtfidfs,qglength = getQgtfidf(queryData)
    """
    cosine similartiy between query and the document has been done. But it is in
    a reverse order, because it does not iterate over the url's, but rather on the words.
    """
    for word in qtfidfs:
        for url in tfidfs[word]:
            if url not in products:
                products[url] = tfidfs[word][url] * qtfidfs[word] /(lengthOftheDoc[url] *qlength)
            else:
                products[url] += tfidfs[word][url] * qtfidfs[word] /(lengthOftheDoc[url] *qlength)
    for genre in qgtfidfs:
        for url in gtfidfs[genre]:
            
            if url not in gproducts:
                gproducts[url] = gtfidfs[genre][url] * qgtfidfs[genre] /(glengthOftheDoc[url] *qglength)
            else:
                gproducts[url] += gtfidfs[genre][url] * qgtfidfs[genre] /(glengthOftheDoc[url] *qglength) 
    
    alpha = 0.95 # this value has been calculated with linear regression.
    
    urls = list(products.keys()) + list(gproducts.keys())
    alphaToAP18 = dict()
    
    sims = {}
    
    ####### Precision: ###################################
    for url in urls:
        v = gv = 0
        if url in products:
            v = products[url]
        if url in gproducts:
            gv = gproducts[url]
        sims[url] = v * alpha + (1-alpha) * gv
        
    sortedSims = {k: v for k, v in sorted(sims.items(), key=lambda item: item[1])[-18:]}
    v=0.0
    recommedTrue = []
    for i in sortedSims:
        if i in queryData["recomms"]:
            v += float(1/18)
            recommedTrue.append(1)
        else:
            recommedTrue.append(0)
    
        
            
    ####### Average Precision: ######################################
    precs = []
    recalls = []
    rchange = []
    temp =0;
    for i in range(18):
        if i != 0:
            temp = recalls[i -1]
            
        precs.append(sum(recommedTrue[:i+1])/(i+1))
        recalls.append(sum(recommedTrue[:i+1])/18)
        rchange.append(recalls[i] - recalls[i-1])
    
    ap18 = 0.0
    for i in range(18):
        ap18 += precs[i]*rchange[i]
    print("\nTitle : " + queryData["title"])
    print("\nAuthor : " + queryData["author"])
    print("\nDescription : " + queryData["desc"])
    print("\n\nGenres : \n")
    [print(genre) for genre in queryData["genres"].keys()]
    print("\n\nRecommendations : \n")
    [print(recomm) for recomm in queryData["recomms"]]
    print("\n\nOur Recommendations : \n")
    [print(doc,sortedSims[doc]) for doc in sortedSims]
    print("AP@18 : ",ap18)
    print("Precision: ",v)
# while alpha < 1:
    
#     sims = {}
    
#     for url in urls:
#         v = gv = 0
#         if url in products:
#             v = products[url]
#         if url in gproducts:
#             gv = gproducts[url]
#         sims[url] = v * alpha + (1-alpha) * gv
        
#     sortedSims = {k: v for k, v in sorted(sims.items(), key=lambda item: item[1])[-18:]}
    
        
#     val = 0.0
#     recommedTrue = []
#     for i in sortedSims:
#         if i in queryData["recomms"]:
#             v += float(1/18)
#             recommedTrue.append(1)
#         else:
#             recommedTrue.append(0)
#     if v >= bestV:
#         bestV = v
#         bestA = alpha
#         theOne = sortedSims
            
#     ##map
#     precs = []
#     recalls = []
#     rchange = []
#     temp =0;
#     for i in range(18):
#         if i != 0:
#             temp = recalls[i -1]
            
#         precs.append(sum(recommedTrue[:i+1])/(i+1))
#         recalls.append(sum(recommedTrue[:i+1])/18)
#         rchange.append(recalls[i] - recalls[i-1])
#     ap18 = 0.0
#     for i in range(18):
#         ap18 += precs[i]*rchange[i]
#     alphaToAP18[alpha] = ap18
#     alpha += 0.005

# sortedp = {k: v for k, v in sorted(products.items(), key=lambda item: item[1])[-18:]}
# sortedgp = {k: v for k, v in sorted(gproducts.items(), key=lambda item: item[1])[-18:]}














