#!/usr/bin/env python3

from dataclasses import dataclass, field

import data
import lexicon
import random

sequences = {
    'base': (
        "subj",
        "subj-a",
        "obj",
        "obj-a",
        "adv",
        "verb",
    ),
    'golden': (
        "subj",
        "obj",
        "verb",
        "subj-a",
        "obj-a",
    ),
    'simple': (
        "subj",
        "obj",
        "verb"
        ),
    'simple_adv': (
        "subj",
        "obj",
        "adv",
        "verb"
        ),
}

@dataclass
class Sentence():
    lexicon: lexicon.Lexicon
    sequence: list[str] = sequences['golden']
    infls: dict = field(default_factory=dict)
    backup_infls: dict = field(default_factory=dict)

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
            word.head += "."
            #revolve infls
            self.backup_infls = self.infls
            self.infls = {}
            self.next_infl = 0

    def remove_word(self):
        self.infls[self.sequence[self.next_infl]] = None
        self.next_infl -= 1
        if (self.next_infl < 0):
            #revolve back
            self.infls = self.backup_infls
            self.next_infl = len(self.sequence) - 1
