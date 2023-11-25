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
temp_verse.goal.append(verse.Foot(["LL", "LS"]))
                      

infl = data.Adjective()
infl.casus = None
infl.gender = None
infl.number = None #data.Number.SINGULAR

possible_meters = temp_verse.get_next_meters(lexicon)
print(len(possible_meters))
while (len(possible_meters) > 0):
    word = lexicon.get_word(possible_meters, [infl])
    #print (word)
    temp_verse.add_word(word)
    possible_meters = temp_verse.get_next_meters(lexicon)
    #print((possible_meters))
    print(str(temp_verse))

print ("line complete")


        

