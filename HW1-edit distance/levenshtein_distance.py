# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 20:51:08 2020

@author: mhrfk
"""

import sys
a = sys.argv[1]
b = sys.argv[2]

#creating an empty table to work on
levenlist = []
for i in range(len(a)+1):
    temp = []
    for j in range(len(b)+1):
        temp.append(0)
    levenlist.append(temp)
#filling the table with the algorithm
for i in range(len(a)+1):
    
    for j in range(len(b)+1):
        if i==0 and j == 0:
            levenlist[i][j] =0
        elif i==0 and j!=0:
            levenlist[i][j] = j
        elif i!=0 and j==0:
            levenlist[i][j] = i
            
        else:
            move = 1
            if a[i-1] == b[j-1]:
                move = 0
            minvalue = min(levenlist[i-1][j] + 1,levenlist[i][j-1] +1,levenlist[i-1][j-1]+move)
            levenlist[i][j] = minvalue
#backtracking
didwhat  = []
i = len(a)
j = len(b)
while True:    
    #ensuring null variables does not damage the test
    temp = levenlist[i][j]
    a = levenlist[i-1][j]
    b = levenlist[i][j-1]
    c = levenlist[i-1][j-1]
    if i == 0:
        a = 99
        c = 99
    if j == 0:
        b = 99
        c = 99
    minvalue = min(a,b,c)
    #backtracking
    if j != 0 and i != 0 and levenlist[i-1][j-1] == minvalue:
        move = "replace"
        i = i-1
        j = j-1
    elif j != 0 and levenlist[i][j-1] == minvalue:
        move = "insert"
        i = i
        j = j-1
    elif i != 0 and levenlist[i-1][j] == minvalue:
        move = "delete"
        i = i-1
        j = j
    else:
        break
    if temp - minvalue ==0:
        didwhat.insert(0, "nothing")
    elif temp - minvalue == 1:
        didwhat.insert(0, move)
    
print("Edit Distance:",levenlist[len(levenlist)-1][len(levenlist[0])-1])
print("Corresponding Edit Table:")
for a in levenlist:
    print(a)
print()
print("Sequnce of the operations needed to get the second string from the first : ",didwhat)
         
         
         
         
         
         
         