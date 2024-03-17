#making a seperate file to load the json file and query the data
#working for only and and or

def andOp(list1,list2): #to implement and operator
    ans = []
    ptr1 = 0 
    ptr2 = 0  

    while ptr1 < len(list1) and ptr2 < len(list2):
        if list1[ptr1] > list2[ptr2]:
            ptr2 += 1
        elif list1[ptr1]<list2[ptr2]:
            ptr1 += 1
        elif list1[ptr1] == list2[ptr2]:
            ans.append(list1[ptr1])
            ptr1 +=1
            ptr2 +=1
    return ans

def orOp(list1, list2): # to implement or operator
    combined_set = set(list1 + list2) # takes out non unique
    ans = list(combined_set)
    return ans            

import nltk
from nltk.stem import PorterStemmer
import json
ps = PorterStemmer()

with open("Index.json","r") as file:
    jsonData = json.load(file)

query = input("Enter query")
query = nltk.word_tokenize(query)
result = []

operators = []
terms = []

for word in query:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        terms.append(word.lower())
    else:
        operators.append(word.lower())

print(terms)
print(operators)

if(len(operators)==0):
    result =jsonData[nltk.word_tokenize(ps.stem(terms[0].casefold()))[0]] # word_tokenize returns a list
    result = list(dict.fromkeys(result))#
    print(result)

else:    
    for ops in operators:

        if ops == 'and':
            del operators[0]
            term1 = terms.pop(0)
            list1 = jsonData[nltk.word_tokenize(ps.stem(term1.casefold()))[0]] # word_tokenize returns a list
            list1 = list(dict.fromkeys(list1))#removing duplicates without compromising on the order
            if (len(result)==0):
                term2 = terms.pop(0)
                list2 = jsonData[nltk.word_tokenize(ps.stem(term2.casefold()))[0]]
                list2 = list(dict.fromkeys(list2))
                result = andOp(list1,list2) ###### 

            else:
                result = andOp(result,list1)####

        elif ops == 'or':
            del operators[0]
            term1 = terms.pop(0)
            list1 = jsonData[nltk.word_tokenize(ps.stem(term1.casefold()))[0]] # word_tokenize returns a list
            list1 = list(dict.fromkeys(list1))#removing duplicates without compromising on the order

            if (len(result)==0):
                term2 = terms.pop(0)
                list2 = jsonData[nltk.word_tokenize(ps.stem(term2.casefold()))[0]]
                list2 = list(dict.fromkeys(list2))
                result = orOp(list1,list2) ###### 

            else:
                result = orOp(result,list1)####


    result.sort()
    print(result)  


