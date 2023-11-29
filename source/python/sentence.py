#!/usr/bin/env python3

from dataclasses import dataclass, field

import data
import lexicon
import random
import sys

sequences = {
    'base': ("subj", "subj-a", "obj", "obj-a", "adv", "verb",),
    'golden': ("subj", "obj", "verb", "subj-a", "obj-a",),
    'simple': ("subj", "obj", "verb",),
    'simple_adv': ("subj", "obj", "adv", "verb",),
    'intj': ("intj",),
}

sequence_weights = {
    'base': 50,
    'golden': 100,
    'simple': 50,
    'simple_adv': 20,
    'intj': 2,
}

sequence_keys = list(sequences.keys())

sentence_stack = []
current_sentence = None

def get_current_sentence():
    global current_sentence
    return current_sentence

def initialize(lexicon):
    global current_sentence
    current_sentence = get_new_sentence(lexicon)

def advance_sentence():
    global current_sentence
    global sentence_stack
    sentence_stack.append(current_sentence)
    current_sentence = get_new_sentence(current_sentence.lexicon)

def rollback_sentence():
    global current_sentence
    global sentence_stack
    temp_sentence = sentence_stack.pop()
    temp_sentence.next_infl = len(temp_sentence.sequence) - 1
    current_sentence = temp_sentence

def get_new_sentence(lexicon):
    sequence_key = random.choices(sequence_keys, weights=[sequence_weights[key] for key in sequence_keys])[0]
    return Sentence(lexicon, sequences[sequence_key])

@dataclass
class Sentence():
    lexicon: lexicon.Lexicon
    sequence: list[str] = sequences['golden']
    infls: dict = field(default_factory=dict)
    next_infl = 0
    
    def get_next_infl(self):
        match(self.sequence[self.next_infl]):
            case("subj"):
                infl = data.Noun()
                infl.casus = data.Casus.NOMINATIVE
                infl.gender = None
                infl.number = None
                return infl
            case("subj-a"):
                subj = self.infls["subj"]
                infl = self.get_adj(subj)
                return infl
            case("obj"):
                infl = data.Noun()
                infl.casus = data.Casus.ACCUSATIVE
                infl.gender = None
                infl.number = None
                return infl
            case("obj-a"):
                obj = self.infls["obj"]
                infl = self.get_adj(obj)
                return infl
            case("verb"):
                subj = self.infls["subj"]
                infl = data.Verb()
                infl.number = subj.number
                infl.person = None
                infl.voice = data.Voice.ACTIVE
                infl.tense = None
                infl.mood = data.Mood.INDICATIVE
                return infl
            case("adv"):
                infl = data.Adverb()
                return infl
            case("intj"):
                infl = data.Interjection()
                return infl
            case _:
                print (self.sequence, self.next_infl, file=sys.stderr)


    def get_adj(self, noun):
        adj = data.Adjective()
        adj.casus = noun.casus
        adj.gender = noun.gender
        adj.number = noun.number
        return adj

    def place_word(self, word):
        #print(word)
        self.infls[self.sequence[self.next_infl]] = word.infl[0]
        if (self.next_infl == 0):
            word.head = word.head.capitalize()
        self.next_infl += 1
        if (self.next_infl >= len(self.sequence)):
            #make it a sentence
            if (len(self.sequence) == 1):
                word.head += "!"
            else:
                word.head +=  "."
            advance_sentence()

    def remove_word(self):
        self.infls[self.sequence[self.next_infl]] = None
        self.next_infl -= 1
        if (self.next_infl < 0):
            rollback_sentence()
