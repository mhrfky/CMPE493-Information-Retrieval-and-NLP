import os
import sys
import string
import math
import random
import copy
#addresses:
root = "./dataset/"
tr_leg = root + "training/legitimate/"
tr_spam = root + "training/spam/"
test_leg = root + "test/legitimate/"
test_spam = root + "test/spam/"

#flags:
puncRemoval = False


#vocabularies
spamVoc = {}    #consists of the tokens and frequencies used in spam mails
legVoc = {}     #consists of the tokens and frequencies used in legitimate mails   
legdistVoc = {} #consists of the tokens and doc frequencies used in spam mails
spamdistVoc= {} #consists of the tokens and doc frequencies used in legitimate mails

#test Results
tests = [[],[],[]]


#variables
alpha = 1
numberOfLegs = 0 #number of legitimate mails
numberOfSpams = 0#number of spam mails
numberOfTotal =0 #number of total mails


"""
@parameter mail : text
@return a text consists of only alphanumerical characters
"""
def extremeRemoval(mail : str):
    newText = ""
    for a in mail:
        if 'a' <= a <= 'z' or 'A' <= a <= 'Z' or '0' <= a <= '9' or a==' ' or a in string.punctuation:
            newText += a
        else:
            newText += " " + a + " "
    if puncRemoval:
        return newText
    return mail

"""
@paremeters 
    mail : text to process
    voc : vocabulary to insert the words' frequncies into
    distVoc : vocabulary to insert the words' doc frequncies into
    
    seperates the "subject", removes the punctiation tokens
    and adds to the frequencies
@return changed voc
"""
def preprocess(mail : str,voc : dict,distVoc : dict):

    mail = mail[8:]
    
    mail = extremeRemoval(mail)
    mail = mail.lower()
    anyTokens = mail.split(' ')
    
    distTokens = list(set(anyTokens))
    for token in distTokens:
        if token in distVoc:
            distVoc[token] += 1
        else:
            distVoc[token]  = 1
    
    for token in anyTokens:
        if token in voc:
            voc[token] += 1
        else:
            voc[token] = 1
    
    voc.pop('')
    distVoc.pop('')
    return voc

"""
    fills the legVoc(vocabulary of the legitimate mails)
"""
def leg_training():
    all_legitimate_training = os.listdir(tr_leg)
    global legVoc
    global numberOfLegs
    global numberOfTotal

    for f in all_legitimate_training:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            numberOfLegs += 1
            numberOfTotal +=1
            mail = open(tr_leg + f,'r').read()
            legVoc = preprocess(mail,legVoc,legdistVoc)
            
"""
    fills the spamVoc(vocabulary of the spam mails)
"""
def spam_training():
    all_spam_training = os.listdir(tr_spam)
    global spamVoc
    global numberOfSpams
    global numberOfTotal
    for f in all_spam_training:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            numberOfSpams += 1
            numberOfTotal +=1
            mail = open(tr_spam + f,'r').read()
            spamVoc = preprocess(mail,spamVoc,spamdistVoc)
            

"""
@parameters
    lvoc: legitimate mails' vocabulary
    svoc: spam mails' vocabulary
    system : which system to use(0:with whole vocabulary, 1:with mutual info)

Does the test on the files in test folder. Uses isLegitimate function to find out
which class it fits into. And store the result in tests list. Prints the rate of
the hits.
"""
def test(lVoc : dict, sVoc : dict,system : int):
    all_legitimate_test =os.listdir(test_leg)
    all_spam_test =os.listdir(test_spam)

    legs = 0
    spams = 0
    legHits = 0
    spamHits = 0
    for f in all_legitimate_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mailR = open(test_leg + f,'r')
            mail = mailR.read()
            mailR.close()
            tests[2].append(1)
            legs+=1
            if isLegitimate(mail,lVoc, sVoc,system):
                tests[system].append(1)
                legHits+=1
            else:
                tests[system].append(0)
                
                
    for f in all_spam_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mailR = open(test_spam + f,'r')
            mail = mailR.read()
            mailR.close()
            tests[2].append(0)
            spams+=1
            if not isLegitimate(mail,lVoc, sVoc,system):
                tests[system].append(0)
                spamHits+=1
            else:
                tests[system].append(1)

    print("For the system ",system)
    print("Legitimate hits: ",legHits,"/",legs)
    print("Spam hits: ",spamHits,"/",spams)
    print("\n\n")
            

"""
@parameters
    mail:   mail to check the class of
    lvoc:   legitimate mails' vocabulary
    svoc:   spam mails' vocabulary
    system: which system to use(0:with whole vocabulary, 1:with mutual info)

Preprocess the mail and checks its class with the given vocabularies with the 
logarithmic formula of:
    cNB = argmax[logP(c j) + logP(xi | c j)

"""
def isLegitimate(mail, lVoc : dict, sVoc : dict,system : int):

    spamPoint = math.log(numberOfSpams/numberOfTotal)
    legPoint  = math.log(numberOfLegs/numberOfTotal)
    
    mail = mail[8:]
    
    mail = extremeRemoval(mail)

    anyTokens = mail.split(" ")

    length = len(list(set(list(sVoc.keys()) + list(lVoc.keys()))))
    legWords = sum(y for x,y in lVoc.items())+alpha* length
    spamWords = sum(y for x,y in sVoc.items())+alpha* length

    # print(legWords,spamWords)
    for token in anyTokens:
        if token in sVoc or token in lVoc:
            pay = (alpha + lVoc[token]) if token in lVoc else alpha
            legPoint += math.log( pay/ legWords )
    
            pay = (alpha + sVoc[token]) if token in sVoc else alpha
            spamPoint += math.log( pay / spamWords)

    return legPoint>=spamPoint




"""
@parameters
    lvoc: legitimate mails' vocabulary
    svoc: spam mails' vocabulary
@return
    lSorted: first 100 tokens with legitimate probabilities
    sSorted: first 100 tokens with spam probabilities
Finds the first 100 words with the X^2 test.
"""
def createFirst100s(lvoc : dict,svoc : dict):
    
    global numberOfLegs
    global numberOfSpams
    global numberOfTotal
    
    global legVoc
    global spamVoc
    
    sPoints = {}
    merged = list(set(list(svoc.keys()) + list(lvoc.keys())))
    for word in merged:
        n11 = 0
        if word in svoc:
            n11 = svoc[word]
        n01 = numberOfSpams - n11
        n10 = 0
        if word in lvoc:
            n10 = lvoc[word]
        n00 = numberOfLegs-n10
        sPoints[word] = (n11 / numberOfTotal) * math.log((1+numberOfTotal*n11)/(1+(n11+n10)*(n11+n01))) + \
                        (n01 / numberOfTotal) * math.log((1+numberOfTotal*n01)/(1+(n01+n00)*(n11+n01))) + \
                        (n10 / numberOfTotal) * math.log((1+numberOfTotal*n10)/(1+(n11+n10)*(n10+n00))) + \
                        (n00 / numberOfTotal) * math.log((1+numberOfTotal*n00)/(1+(n01+n00)*(n00+n10)))
               
    sSorted =  {k: spamVoc[k] if k in spamVoc else 0 for k, v in sorted(sPoints.items(), key=lambda x: x[1], reverse=True)[:100]}
    lSorted =  {k: legVoc[k] if k in legVoc else 0 for k, v in sorted(sPoints.items(), key=lambda x: x[1], reverse=True)[:100]}

    return lSorted,sSorted




"""
@parameters
    test: list of the results from the systems and correct ones
    system : which system to evaluate(0:with whole vocabulary, 1:with mutual info)
@returns
    P : precision
    R : recall
    F : f value
"""
def evaluateResults(test,system : int):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(numberOfTotal):
        if test[system][i] == 1 and test[2][i] == 1:
            tp += 1
        elif test[system][i] == 1 and test[2][i] == 0:
            fp += 1
        elif test[system][i] == 0 and test[2][i] == 1:
            fn += 1
        elif test[system][i] == 0 and test[2][i] == 0:
            tn += 1
    P = tp/(tp+fp)
    R = tp/(tp+fn)
    F = 2*P*R/(P+R)
    return P,R,F

"""
Does the randomization test with a shuffling probability of 0.5
"""
def copyByAppend(lsit):
    temp = [[],[],[]]
    a = -1
    for i in lsit:
        a+=1
        for j in i:
            temp[a].append(j)
    return temp
            
def randomizationTest():
    global tests
    
    p0,r0,f0 = evaluateResults(tests,0)
    print("System with the whole vocabulary has:\n",
          "Precision :",p0,"\n" ,
          "Recall :",r0,"\n" ,
          "F score :",f0)
    print("\n\n\n")

    p1,r1,f1 = evaluateResults(tests,1)
    print("System with the mutual info of 100 tokens has:\n",
          "Precision :",p1,"\n" ,
          "Recall :",r1,"\n" ,
          "F score :",f1)
    S = abs(f0-f1)
    print("\n\n\n")

    counter = 0
    R = 1000
    print("Testing with R value as",R)
    for j in range(R):
        # temp = [i for i in tests]
        # temp = tests
        # temp = tests.copy()
        # temp = [[j for j in i] for i in tests]
        # temp = copyByAppend(tests)
        temp = copy.deepcopy(tests)
        for i in range(numberOfTotal):
            

            v = random.randint(0, 1)
            if v == 0:
                val = temp[0][i]
                temp[0][i] = temp[1][i]
                temp[1][i] = val
                
            else:
                continue
        p0,r0,f0 = evaluateResults(temp,0)
        p1,r1,f1 = evaluateResults(temp,1)
        S_ = abs(f0-f1)
        if S_ >= S:
            counter+=1
    P = (counter+1)/(R+1)
    if P <= 0.05:
        print("Rejected with the P value as",P)
    else:
        print("Approved with the P value as",P)



#training
leg_training()
spam_training()
#test for the whole vocabulary
test(legVoc,spamVoc,0)

#creation of 100 tokens vocabulary
lSorted,sSorted =createFirst100s(legdistVoc, spamdistVoc)
#test for the latter vocabulary
test(lSorted,sSorted,1)


randomizationTest()





















    