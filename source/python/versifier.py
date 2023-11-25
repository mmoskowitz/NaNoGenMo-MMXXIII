#!/usr/bin/env python3

import sys,re, copy
import scanner
import data
import verse
import lexicon


filename = sys.argv[1]

lexicon = lexicon.Lexicon()

debug = True

#read content
with open(filename) as file:
    i = 0
    for line in file:
        i+= 1
        lexicon.parse_line(line)
        if (i % 50000 == 0):
            print (i)
            if (debug and i > 200000):
                break

#print (len(lexicon.infls))
#print ("/n".join([(str(infl) + str(type(infl))) for infl in lexicon.infls]))
            
temp_verse = verse.Verse()
for i in range(4):
    temp_verse.goal.append(verse.Foot(["LSS","LL"]))
temp_verse.goal.append(verse.Foot(["LSS"]))
temp_verse.goal.append(verse.Foot(["LL"]))
                      

infl = data.Noun()
infl.casus = None
infl.gender = None
infl.number = None #data.Number.SINGULAR
meters = [
    "VLSV",
    "CSLSV",
    "CSLV",
    "CLLV",
    "CLLSC",
    "VSLLC",
    ]
for meter in meters:
    word = lexicon.get_word([meter], [infl])
    #print (word)
    temp_verse.add_word(word)
    print (temp_verse.check_meter(temp_verse.current))

print(str(temp_verse))
        

