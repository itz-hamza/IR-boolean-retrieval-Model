import nltk
from nltk.stem import PorterStemmer
import json

ps = PorterStemmer()
Index={}
PositionalIndex={}
files = [1,2,3,7,8,9,11,12,13,14,15,16,17,18,21,22,23,24,25,26]# there are several files, and reading them individually was boring, so i made a list with each element representing file name. i will loop over each element, and open it's corresponding file

sList = [] # a list which will have all the stop words
with open(r"Stopword-List.txt") as stopList:
    words = stopList.readlines() 
    for word in words:
        sList.append(word.strip()) # since each stop word was having \n at the end of it, i used strip method to strip it off

for fileNumber in files:
    i=0 # this i represents position of a word in it's document. 
    with open(f"{fileNumber}.txt",'r') as file:
        sentences = file.readlines() # breaking each file in a set of sentences
        for line in sentences: # for each sentence in the sentence set
            words = nltk.word_tokenize(line) #tokenizing each sentence in a set of tokens
            for word in words: # iterating over a set of tokens
                word = ps.stem(word.casefold())  # stemming and casefolding each token
                if word not in sList and word[0].isalpha(): # terms starting with a number shall be skipped
                    if word in PositionalIndex: #if a term already exists, then append the doc id in its posting list
                        PositionalIndex[word].append((f"{fileNumber}",i))  #in positional index, append doc id along with its position
                        Index[word].append(f"{fileNumber}") 
                    else:
                        PositionalIndex[word] = [(f"{fileNumber}",i)]
                        Index[word] = [(f"{fileNumber}")]
                i=i+1 # for position

for term,docId in list(PositionalIndex.items()):  #deleting the terms that occur less than 2 times. I decided the number to be 2 because lower than 2 there weren't much deletions
    freq = len(docId)
    if freq <= 2:
        del PositionalIndex[term]

for term,docId in list(Index.items()):  #doing the same for this index as well 
    freq = len(docId)
    if freq <= 2:
        del Index[term]


file_path = 'PositionalIndex.json'

# Write dictionary to file
with open(file_path, 'w') as file: # making a json file to store the dictionary
    json.dump(PositionalIndex, file)

file_path = 'Index.json'
with open(file_path, 'w') as file: # making a json file to store the dictionary
    json.dump(Index, file)

print(Index['overview'])

# with open(r'Positionalterms.txt','w') as file:
#     for keys in PositionalIndex:
#         file.write(f"{keys} {len(PositionalIndex[keys])} \n")

# with open(r'terms.txt','w') as file:
#     for keys in Index:
#         file.write(f"{keys} {len(Index[keys])} \n")