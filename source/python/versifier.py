#!/usr/bin/env python3

import sys,re, copy
import scanner
import data
import verse
import lexicon


filename = sys.argv[1]

lexicon = lexicon.Lexicon()

debug = False

#read content
with open(filename) as file:
    i = 0
    for line in file:
        i+= 1
        lexicon.parse_line(line)
        if (i % 50000 == 0):
            print (i)
            if (debug and i > 100000):
                break

#print (len(lexicon.infls))
#print ("/n".join([(str(infl) + str(type(infl))) for infl in lexicon.infls]))
            
base_verse = verse.Verse()
base_verse.goal.append(verse.Foot(["LSS","LL"]))
base_verse.goal.append(verse.Foot(["LSS","LL"]))
base_verse.goal.append(verse.Foot(["LSS","LL"], caesura=True))
base_verse.goal.append(verse.Foot(["LSS","LL"]))
base_verse.goal.append(verse.Foot(["LSS"]))
base_verse.goal.append(verse.Foot(["LL", "LS"], diaeresis=True))
print (" ".join(str(foot) for foot in base_verse.goal))
                      

infl_adj = data.Adjective()
infl_adj.casus = None
infl_adj.gender = None
infl_adj.number = None #data.Number.SINGULAR

infl_verb = data.Verb()
infl_verb.number = None
infl_verb.person = None
infl_verb.voice = None
infl_verb.tense = None
infl_verb.mood = None


def build_line(temp_verse, lexicon):
    possible_meters = temp_verse.get_next_meters(lexicon)        
    if (len(possible_meters) == 0):
        if (temp_verse.check_meter("", True)):
            return temp_verse
        else:
            return None
    global infl_verb
    while (len(possible_meters) > 0):
        word = lexicon.get_word(possible_meters, [infl_verb])
        if (word is None):
            return None
        if (len(word.head) < 4):
            possible_meters.remove(word.meter)
            continue
        new_verse = copy.deepcopy(temp_verse)
        new_verse.add_word(word)
        print("trying ", new_verse)
        try_verse = build_line(new_verse, lexicon)
        if (try_verse is not None):
            return try_verse
        else:
            possible_meters.remove(word.meter)
            continue
    return None

for i in range(30):
    temp_verse = build_line(base_verse,lexicon)
    if (temp_verse is not None):
        print (temp_verse)
    


        

