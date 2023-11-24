#!/usr/bin/env python3

import sys,re, copy
import scanner
import data
import verse
import lexicon


filename = sys.argv[1]

lexicon = lexicon.Lexicon()

#read content
with open(filename) as file:
    i = 0
    for line in file:
        i+= 1
        lexicon.parse_line(line)
        if (i % 50000 == 0):
            print (i)

#print (len(lexicon.infls))
#print ("/n".join([(str(infl) + str(type(infl))) for infl in lexicon.infls]))
            
verse = verse.Verse()

infl = data.Noun()
infl.casus = None
infl.gender = None
infl.number = data.Number.SINGULAR
for i in range(6):
    word = lexicon.get_word(["CLSSV"], [infl])
    print (word)
    verse.add_word(word)

print(str(verse))
        

