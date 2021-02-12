import os
import string
root = "./dataset/"
tr_leg = root + "training/legitimate/"
tr_spam = root + "training/spam/"
test_leg = root + "test/legitimate/"
test_spam = root + "test/spam/"

puncRemoval = False
alpha = 1
unWantedTokens = ["'s","'d","'m","'re"]
legitimateNumber  = 0
spamNumber = 0
vocabulary = {}

# debug: comment below
firstKleg = []
firstKspam = []
def tokenCheck(token : str):
    return True#token not in string.punctuation and token not in unWantedTokens
def punc_removal(mail : str):
    mail = mail.replace("\n","")
    mail = mail.replace("\t","")

    for punc in string.punctuation:
        mail = mail.replace(punc,"")
    return mail
def extremeRemoval(mail : str):
    newText = ""
    for a in mail:
        if 'a' <= a <= 'z' or 'A' <= a <= 'Z' or '0' <= a <= '9' or a==' ':
            newText += a
    if puncRemoval:
        return newText
    return mail
        
def Lpreprocess(mail : str):
    global legitimateNumber
    global spamNumber
    mail = mail[8:]
    
    mail = extremeRemoval(mail)
    
    anyTokens = mail.split(' ')


    
    for token in anyTokens:
        if tokenCheck(token):
            legitimateNumber += 1
            if token in vocabulary:
                vocabulary[token][0] += 1
            else:
                vocabulary[token] = [alpha+1,alpha]
                legitimateNumber += 1
                spamNumber += 1
    
def Spreprocess(mail : str):
    global legitimateNumber
    global spamNumber
    mail = mail[8:]
    
    mail = extremeRemoval(mail)


    anyTokens = mail.split(' ')


    
    for token in anyTokens:
        if tokenCheck(token):
            spamNumber += 1
            if token in vocabulary:
                vocabulary[token][1] += 1
            else:
                vocabulary[token] = [alpha,alpha+1]
                legitimateNumber += 1
                spamNumber += 1
    
            
            
def leg_training():
    all_legitimate_training = os.listdir(tr_leg)
    
    for f in all_legitimate_training:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mail = open(tr_leg + f,'r').read()
            Lpreprocess(mail)
            
def spam_training():
    all_spam_training = os.listdir(tr_spam)
    
    for f in all_spam_training:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mail = open(tr_spam + f,'r').read()
            Spreprocess(mail)
            
            


def test1():
    all_legitimate_test =os.listdir(test_leg)
    all_spam_test =os.listdir(test_spam)
    legs = 0
    legHits = 0
    spams = 0
    spamHits = 0
    for f in all_legitimate_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mailR = open(test_leg + f,'r')
            mail = mailR.read()
            mailR.close()
            if isLegitimate(mail):
                legHits += 1
            legs += 1
    for f in all_spam_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mail = open(test_spam + f,'r').read()
            if not isLegitimate(mail):
                spamHits += 1
            spams += 1
    print("Legitimate hit rate:" , legHits,"/",legs)
    print("Spam hit rate:" , spamHits,"/",spams)
def test2():
    global firstKleg
    global firstKspam



    all_legitimate_test =os.listdir(test_leg)
    all_spam_test =os.listdir(test_spam)
    
    legs = 0
    legHits = 0
    spams = 0
    spamHits = 0
    for f in all_legitimate_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mailR = open(test_leg + f,'r')
            mail = mailR.read()
            mailR.close()
            if isLegitimate2(mail):
                legHits += 1
            legs += 1
    for f in all_spam_test:     #read all the files with .sgm extension
        if f[-4:] == ".txt":
            mail = open(test_spam + f,'r').read()
            if not isLegitimate2(mail):
                spamHits += 1
            spams += 1    
    print("Legitimate hit rate:" , legHits,"/",legs)
    print("Spam hit rate:" , spamHits,"/",spams)
        
def isLegitimate(mail):
    global legitimateNumber
    global spamNumber
    spamPoint = 1
    legPoint = 1
    
    mail = mail[8:]
    
    mail = extremeRemoval(mail)

    tempWordsCount = 0
    anyTokens = mail.split(' ')

    
    
    for token in anyTokens:
        if token in vocabulary:
            legPoint *= vocabulary[token][0] /legitimateNumber
            spamPoint*= vocabulary[token][1] /spamNumber
        else:
            legPoint/=legitimateNumber
            spamPoint/=spamNumber

    
    return spamPoint <= legPoint
def isLegitimate2(mail):
    global legitimateNumber
    global spamNumber
    spamPoint = 1
    legPoint = 1
    
    mail = mail[8:]
    
    mail = extremeRemoval(mail)

    tempWordsCount = 0
    anyTokens = mail.split(' ')

    
    
    for token in anyTokens:
        if token in firstKleg:
            legPoint *= firstKleg[token][0] /100
        else:
            legPoint/=legitimateNumber

        if token in firstKspam:
            spamPoint*= firstKspam[token][1] /100
        else:
            spamPoint/=spamNumber

    
    return spamPoint <= legPoint
leg_training()
spam_training()

firstKleg =  {k: v for k, v in sorted(vocabulary.items(), key=lambda x: x[1][0] / x[1][1], reverse=True)[:100]}
firstKspam = {k: v for k, v in sorted(vocabulary.items(), key=lambda x: x[1][1] / x[1][0], reverse=True)[:100]}


test1()

test2()


                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        