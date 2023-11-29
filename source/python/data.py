#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, EnumMeta
import copy



#from https://stackoverflow.com/questions/43634618/how-do-i-test-if-int-value-exists-in-python-enum-without-using-try-catch
class MyEnumMeta(EnumMeta):  
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

class Feature(Enum, metaclass=MyEnumMeta):

    def __str__(self):
        return self.value;
        
class Casus(Feature):
    NOMINATIVE = "nom"
    GENITIVE = "gen"
    DATIVE = "dat"
    ACCUSATIVE = "acc"
    ABLATIVE = "abl"
    VOCATIVE = "voc"
    LOCATIVE = "loc"

class Number(Feature):
    SINGULAR = "s"
    PLURAL = "p"

class Gender(Feature):
    MASCULINE = "m"
    FEMININE = "f"
    NEUTER = "n"

class Person(Feature):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"

class Tense(Feature):
    PRESENT = "pres"
    PERFECT = "perf"
    IMPERFECT = "impf"

class Voice(Feature):
    ACTIVE = "actv"
    PASSIVE = "pasv"
    
class Mood(Feature):
    INDICATIVE = "indc"
    SUBJUNCTIVE = "sub"
    IMPERATIVE = "impr"

@dataclass
class Grammar:
    def set_feature(self, feature):
        pass

    
    """
    returns true if the defined features in x match self
    """
    def matches(self, x): return False

    def __hash__(self): return hash(str(self))
    def __eq__(self, x): return str(self)==str(x)
    def __ne__(self, x): return str(self)!=str(x)


@dataclass
class Word:
    head: str = None # actual headword
    pos: str = None # part of speech
    meter: str = "" # meter of word
    infl: list[Grammar] = field(default_factory=list)
    text: str = None # is this used?
    page: str = None # ascii version of word

    @classmethod
    def parse_line(cls, line):
        parts = line.split(',')
        (head, meter, pos, inflcode) = parts[0:4]
        debug = False # (head == "culmina")
        infl = copy.deepcopy(pos_to_grammar(pos))
        for featurecode in inflcode.strip().split('-'):
            feature = string_to_feature(featurecode)
            if (debug):
                print (featurecode, feature)
            infl.set_feature(feature)
        word = Word(head, pos, meter, [infl])
        if (debug):
            print (word, line)
        return word
        
    
@dataclass
class Template:
    name: str = None
    args: list[str] = field(default_factory=list)
    params: dict = field(default_factory = lambda: {})

@dataclass
class Noun(Grammar):
    gender: Gender = Gender.MASCULINE
    casus: Casus = Casus.NOMINATIVE
    number: Number = Number.SINGULAR

    def set_feature(self, feature):
        if (not(isinstance(feature, Grammar))):
            feature = string_to_feature(feature)
        match(feature):
            case Gender():
                self.gender = feature
            case Casus():
                self.casus = feature
            case Number():
                self.number = feature

    def __str__(self):
        return "-".join((str(self.gender), str(self.casus), str(self.number)))

    def matches(self, x):
        if not(isinstance(x, Noun)):
            return False
        if (x.gender is not None and x.gender != self.gender):
            return False
        if (x.casus is not None and x.casus != self.casus):
            return False
        if (x.number is not None and x.number != self.number):
            return False
        return True
        
    def __hash__(self): return hash("n:" + str(self))
    def __eq__(self, x): return isinstance(x, Noun) and str(self)==str(x)
    def __ne__(self, x): return not(isinstance(x, Noun)) or str(self)!=str(x)
    
@dataclass
class Adjective(Grammar):
    gender: Gender = Gender.MASCULINE
    casus: Casus = Casus.NOMINATIVE
    number: Number = Number.SINGULAR

    def set_feature(self, feature):
        if (not(isinstance(feature, Grammar))):
            feature = string_to_feature(feature)
        match(feature):
            case Gender():
                self.gender = feature
            case Casus():
                self.casus = feature
            case Number():
                self.number = feature

    def __str__(self):
        return "-".join((str(self.gender), str(self.casus), str(self.number)))

    def matches(self, x):
        if not(isinstance(x, Adjective)):
            return False
        if (x.gender is not None and x.gender != self.gender):
            return False
        if (x.casus is not None and x.casus != self.casus):
            return False
        if (x.number is not None and x.number != self.number):
            return False
        return True
        
    def __hash__(self): return hash("adj:" + str(self))
    def __eq__(self, x): return isinstance(x, Adjective) and str(self)==str(x)
    def __ne__(self, x): return not(isinstance(x, Adjective)) or str(self)!=str(x)

@dataclass
class Adverb(Grammar):

    def __str__(self):
        return "adv"
    
    def matches(self, x):
        if not(isinstance(x, Adverb)):
            return False
        return True
        
    def __hash__(self): return hash("adv:" + str(self))
    def __eq__(self, x): return isinstance(x, Adverb) and str(self)==str(x)
    def __ne__(self, x): return not(isinstance(x, Adverb)) or str(self)!=str(x)

@dataclass
class Interjection(Grammar):

    def __str__(self):
        return "intj"
    
    def matches(self, x):
        if not(isinstance(x, Interjection)):
            return False
        return True
        
    def __hash__(self): return hash("intj:" + str(self))
    def __eq__(self, x): return isinstance(x, Interjection) and str(self)==str(x)
    def __ne__(self, x): return not(isinstance(x, Interjection)) or str(self)!=str(x)

    
@dataclass
class Verb(Grammar):
    person: Person = Person.FIRST
    number: Number = Number.SINGULAR
    tense: Tense = Tense.PRESENT
    voice: Voice = Voice.ACTIVE
    mood: Mood = Mood.INDICATIVE

    def set_feature(self, feature):
        if (not(isinstance(feature, Grammar))):
            feature = string_to_feature(feature)
        match(feature):
            case Person():
                self.person = feature
            case Number():
                self.number = feature
            case Tense():
                self.tense = feature
            case Voice():
                self.voice = feature
            case Mood():
                self.mood = feature
                
    def __str__(self):
        return "-".join((str(self.person), str(self.number), str(self.tense), str(self.voice), str(self.mood)))

    def matches(self, x):
        if not(isinstance(x, Verb)):
            return False
        if (x.person is not None and x.person != self.person):
            return False
        if (x.number is not None and x.number != self.number):
            return False
        if (x.tense is not None and x.tense != self.tense):
            return False
        if (x.voice is not None and x.voice != self.voice):
            return False
        if (x.mood is not None and x.mood != self.mood):
            return False
        return True
        
    def __hash__(self): return hash("v:" + str(self))
    def __eq__(self, x): return isinstance(x, Verb) and str(self)==str(x)
    def __ne__(self, x): return not(isinstance(x, Verb)) or str(self)!=str(x)

    
#default grammar value for each pos
grammar_from_pos = {
    "pn": Noun(),
    "n": Noun(),
    "v": Verb(),
    "part": Adjective(),
    "adj": Adjective(),
    "adv": Adverb(),
    "intj": Interjection(),
    }

def pos_to_grammar(pos):
    if (pos not in grammar_from_pos):
        return Grammar()
    else:
        return grammar_from_pos[pos]

def string_to_feature(value):
    if (value in Casus):
        return Casus(value)
    if value in Number:
        return Number(value)
    if value in Gender:
        return Gender(value)
    if value in Person:
        return Person(value)
    if value in Tense:
        return Tense(value)
    if value in Voice:
        return Voice(value)
    if value in Mood:
        return Mood(value)
    return None
    
