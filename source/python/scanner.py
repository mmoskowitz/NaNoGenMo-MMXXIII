#!/usr/bin/env python3

import re, sys

debug = False

tests = [
    "a",
    "ab",
    "aba",
    "hava",
    "6ta",
    "za",
    "claba",
    "skama",
    'maz',
    'zam',
    'aequeo',
    'Abalōrum',
    'coquum',
    ]

LONG_CODE = "@"
long_vowels = 'ĀāĂĒēĩĪīŌōũŪūȲȳÆæŒœ'
short_vowels = "aeiouyAEIOUY"
vowels = long_vowels + short_vowels
long_consonants = "xzXZ"
short_consonants = 'bcdfghjklmnqprstvwBCDFGHJKLMNQPRSTVW'
consonants = long_consonants + short_consonants
letters = vowels + consonants
mutes = "bcdgptBCDGPT"
liquids = "lr"
mlre = re.compile("[{0}][{1}][{2}]$".format(vowels, mutes, liquids)) # mute+liquid
lcre = re.compile("[{0}][{1}]$".format(vowels, long_consonants)) # long cons
mcre = re.compile("[{0}][{1}][{1}]+$".format(vowels, consonants)) # many cons
lvre = re.compile("[{0}{1}]".format(long_vowels, LONG_CODE)) # long vowels
hvre = re.compile("[{0}]".format(vowels)) #has vowels
evre = re.compile("[{0}]$".format(vowels)) #ends with vowel
emre = re.compile("[{0}]m$".format(vowels)) #ends with m
elre = re.compile("[{0}]$".format(long_consonants)) #ends with a long consonant
eccre = re.compile("[{0}][{0}]$".format(consonants)) #ends with many consonants
ignores = "hH"
diphthongs = ["ae", "au", "ei", "eu", "oe", "Ae", "Au", "Ei", "Eu", "Oe",]
short_clusters = ["qu", "Qu"]
for b in mutes:
    for r in liquids:
        short_clusters.append(b+r) #makes mute-liquid always short (for now)


"""Produces a code that looks like SF...E where S (start) is  v/c/m/x, F (foot) is l/s/a, and E (end) is v/c/x"""
def scan_text(text):
    feet = ""
    start = "" # start code
    end = "" # end code
    current = "" #current foot being built
    is_start = True
    for l in text:
        if not (l in letters):
            if (debug):
                print ("non-letter in word: " + l, file=sys.stderr)
            continue
        if (l in ignores):
            continue

        is_vowel = l in vowels
        is_cons = not(is_vowel)
        #print (current + ":" + l)

        if (is_start): #starts
            if ((current + l) in short_clusters): #cluster
                start = "C"
                current = ""
                is_start = False
            elif (is_vowel):
                if (current == ""): #start with vowel
                    start = "V"
                elif (current in long_consonants): #start with long cons
                    start = "X"
                elif (len(current) == 1): #start with short cons
                    start = "C"
                else: #start with many cons
                    start = "X"
                current = l
                is_start = False
            else: #starts with cons
                current += l
                # is_start is still True
        else: #not start
            if (current == ""):
                current = l
                continue
            if (is_vowel):
                if (current.endswith("q") and l == "u"): #skip u after q
                    current = current[:-1] + "c" #but only once
                    continue 
                if ((current + l) in diphthongs): #diphthong
                    current += LONG_CODE
                    current += l
                elif (current):
                    #new foot
                    feet += new_foot(current)
                    current = l
            else: #is consonant
                current += l
    #last foot
    if (hvre.search(current)):
        feet += new_foot(current)

    #deal with end
    if (emre.search(current) is not None):
        end = "M"
    elif (evre.search(current) is not None):
        end = "V"
    elif (elre.search(current) is not None):
        end = "X"
    elif (eccre.search(current) is not None):
        end = "X"
    else:
        end = "C"
        
    return "".join((start,feet,end))

def new_foot(syllable):
    if (lvre.search(syllable) is not None):
        return "L"
    if (mlre.search(syllable) is not None):
        return "S"
    if (lcre.search(syllable) is not None):
        return "L"
    if (mcre.search(syllable) is not None):
        return "L"
    return "S"

if (0):
    for test in tests:
        print (test)
        print (scan_text(test))
