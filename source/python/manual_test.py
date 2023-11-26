#!/usr/bin/env python3

import sys,re, copy
import scanner
import data
import verse
import lexicon

temp_verse = verse.Verse()
temp_verse.goal.append(verse.Foot(["LSS","LL"]))
temp_verse.goal.append(verse.Foot(["LSS","LL"]))
temp_verse.goal.append(verse.Foot(["LSS","LL"], caesura=True))
temp_verse.goal.append(verse.Foot(["LSS","LL"]))
temp_verse.goal.append(verse.Foot(["LSS"]))
temp_verse.goal.append(verse.Foot(["LL", "LS"], diaeresis=True))

temp_verse.current = "LS SLS SL LL L LSS LLC"
print (temp_verse)
print (temp_verse.check_meter(""))
print (temp_verse.check_meter("", True))
