#!/usr/bin/env python3

import sys,re, copy
import scanner
import data
import verse
import lexicon
import sentence


filename = sys.argv[1]
lines = 5
if (len(sys.argv) > 2):
    lines = int(sys.argv[2])

lexicon = lexicon.Lexicon()

debug = False

#read content
with open(filename) as file:
    i = 0
    for line in file:
        i+= 1
        lexicon.parse_line(line)
        if (i % 50000 == 0):
            #print (i)
            if (debug and i > 100000):
                break

#print (len(lexicon.infls))
#print ("/n".join([(str(infl) + str(type(infl))) for infl in lexicon.infls]))
            
base_hexameter = verse.Verse()
base_hexameter.goal.append(verse.Foot(["LSS","LL"]))
base_hexameter.goal.append(verse.Foot(["LSS","LL"]))
base_hexameter.goal.append(verse.Foot(["LSS","LL"], caesura=True))
base_hexameter.goal.append(verse.Foot(["LSS","LL"]))
base_hexameter.goal.append(verse.Foot(["LSS"]))
base_hexameter.goal.append(verse.Foot(["LL", "LS"], diaeresis=True))
#print (" ".join(str(foot) for foot in base_verse.goal))
                      
temp_sentence = sentence.Sentence(lexicon)



def build_line(temp_verse, lexicon):
    global temp_sentence
    possible_meters = temp_verse.get_next_meters(lexicon)
    #print (len(possible_meters))
    if (len(possible_meters) == 0):
        if (temp_verse.check_meter("", True)):
            return temp_verse
        else:
            return None
    while (len(possible_meters) > 0):
        infl = temp_sentence.get_next_infl()
        #print (len(possible_meters), infl)
        word = lexicon.get_word(possible_meters, [infl])
        if (word is None):
            return None
        new_verse = copy.deepcopy(temp_verse)
        #print ("Placing ", word)
        temp_sentence.place_word(word)
        new_verse.add_word(word)
        #print("trying ", new_verse)
        try_verse = build_line(new_verse, lexicon)
        if (try_verse is not None):
            return try_verse
        else:
            possible_meters.remove(word.meter)
            #print ("Removing ", word)
            temp_sentence.remove_word()
            continue
    return None

for i in range(lines):
    temp_verse = build_line(base_hexameter,lexicon)
    if (temp_verse is not None):
        print (temp_verse)
    


        

