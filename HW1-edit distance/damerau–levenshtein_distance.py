# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:32:54 2020

@author: mhrfk
"""
import sys
a = sys.argv[1]
b = sys.argv[2]


#creating empth tables to work on
levenlist = []
moves = []
for i in range(len(a)+1):
    temp = []
    for j in range(len(b)+1):
        temp.append(0)
    levenlist.append(temp)
for i in range(len(a)+1):
    temp = []
    for j in range(len(b)+1):
        temp.append(0)
    moves.append(temp)
    
#filling the levenlist table accordingly to the algorithm
# filling the moves table accordingly to the directions followed on the previous table
for i in range(len(a)+1):
    
    for j in range(len(b)+1):
        if i==0 and j == 0:
            levenlist[i][j] =0
        elif i==0 and j!=0:
            levenlist[i][j] = j
            moves[i][j] = "j"
        elif i!=0 and j==0:
            levenlist[i][j] = i
            moves[i][j] = "i"
        else:
            move = 1
            if a[i-1] == b[j-1]:
                move = 0
            minvalue = min(levenlist[i-1][j] +1,
                           levenlist[i][j-1] +1,
                           levenlist[i-1][j-1]+move)
            
            levenlist[i][j] = minvalue
            if i > 1 and j > 1 and a[i-1]==b[j-2] and a[i-2] == b[j-1]: 
                levenlist[i][j] = min(levenlist[i][j], levenlist[i-2][j-2] + 1)

            if minvalue == levenlist[i-2][j-2] + 1 and a[i-1]==b[j-2] and a[i-2] == b[j-1]:
                moves[i][j]=("ijij")
            elif minvalue == levenlist[i-1][j-1] + move:
                moves[i][j]=("ij")
            elif minvalue == levenlist[i][j-1] + 1:
                moves[i][j]=("j")
            elif minvalue == levenlist[i-1][j] + 1:
                moves[i][j]=("i")
            else:
                moves[i][j]=(minvalue)
                
#following the directions and difference between the regarding unit squares to
#find appropriate sequence of moves needed to get the second string
didwhat = []
i = len(a)
j = len(b)
while True:
    temp = levenlist[i][j]
    if moves[i][j] == "i":
        i = i-1
        move = "delete"
    elif moves[i][j] == "j":
        j= j-1
        move = "insert"

    elif moves[i][j] == "ij":
        i= i -1
        j = j-1
        move = "replace"

    elif moves[i][j] == "ijij":
        i = i-2
        j = j-2
        move = "swap"
    if levenlist[i][j] - temp == 0:
        didwhat.insert(0,"nothing")
    else:
        didwhat.insert(0,move)
    if i==0 and j==0:
        break
print("Edit Distance:",levenlist[len(levenlist)-1][len(levenlist[0])-1])
print("Corresponding Edit Table:")
for a in levenlist:
    print(a)
print()
print("Sequnce of the operations needed to get the second string from the first : ",didwhat)