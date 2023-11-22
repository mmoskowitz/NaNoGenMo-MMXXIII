#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, EnumMeta

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

class Voice(Feature):
    ACTIVE = "actv"
    PASSIVE = "pass"
    
class Mood(Feature):
    INDICATIVE = "indc"
    SUBJUNCTIVE = "subj"

@dataclass
class Grammar:
    def set_feature(self, feature):
        pass


@dataclass
class Word:
    head: str = None # actual headword
    pos: str = None # part of speech
    meter: str = "" # meter of word
    infl: list[Grammar] = field(default_factory=list)
    text: str = None
    page: str = None # ascii version of word
    
@dataclass
class Template:
    name: str = None
    args: list[str] = field(default_factory=list)
    params: dict = field(default_factory = lambda: {})

@dataclass
class Noun(Grammar):
    gender: Gender = Gender.NEUTER
    casus: Casus = Casus.NOMINATIVE
    number: Number = Number.SINGULAR

    def set_feature(self, feature):
        match(feature):
            case Gender():
                self.gender = feature
            case Casus():
                self.casus = feature
            case Number():
                self.number = feature

    def __str__(self):
        return "-".join((str(self.gender), str(self.casus), str(self.number)))

@dataclass
class Adjective(Noun):
    pass

@dataclass
class Verb(Grammar):
    person: Person = Person.FIRST
    number: Number = Number.SINGULAR
    tense: Tense = Tense.PRESENT
    voice: Voice = Voice.ACTIVE
    mood: Mood = Mood.INDICATIVE

    def set_feature(self, feature):
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

    
#default grammar value for each pos
grammar_from_pos = {
    "pn": Noun(),
    "n": Noun(),
    "v": Verb(),
    "adj": Adjective(),
    }

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
    return None
    
