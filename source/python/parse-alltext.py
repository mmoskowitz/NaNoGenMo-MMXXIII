#!/usr/bin/env python3

import sys,re, copy
from dataclasses import dataclass, field
from enum import Enum, EnumMeta
import scanner

filename = sys.argv[1]

linecount = 0
maxlines = 32000

output_lines = []

pos_headings = {
    "Adjective": "adj",
    "Adverb": "adv",
    "Article": "art",
    "Conjunction": "conj",
    "Determiner": "det",
    "Gerund": "ger",
    "Idiom": "idi",
    "Interjection": "intj",
    "Noun": "n",
    "Numeral": "num",
    "Participle": "part",
    "Postposition": "postp",
    "Preposition": "prep",
    "Prepositional phrase": "prep-phr",
    "Pronoun": "pron",
    "Proper noun": "pn",
    "Verb": "v",
    }

pos_from_head = {
    "adjective form": "adj",
    "adjective": "adj",
    "adverb form": "adv",
    "adverb": "adv",
    "article form": "art",
    "article": "art",
    "conjuction": "conj",
    "conjunction": "conj",
    "contraction": "cont",
    "determiner form": "det",
    "determiner": "def",
    "diacritical mark": "dia",
    "gerund form": "ger",
    "idiom": "idi",
    "interjection": "intj",
    "letter": "let",
    "misspelling": "miss",
    "noun forms": "n",
    "noun form": "n",
    "nouns": "n",
    "noun": "n",
    "numeral form": "num",
    "numeral": "num",
    "participle form": "part",
    "participle": "part",
    "particle": "xxx",
    "phrases": "xxx",
    "phrase": "xxx",
    "postposition": "postp",
    "prefix form": "xxx",
    "prefixes": "xxx",
    "prefix": "xxx",
    "prepositional phrase": "prep-p",
    "preposition": "prep",
    "pronoun form": "pron",
    "pronoun": "pron",
    "proper noun form": "pn",
    "proper noun": "pn",
    "proverb": "xxx",
    "symbol": "xxx",
    "verb form": "v",
    "verb": "v",
}

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
    pass
        
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
    FIRST = 1
    SECOND = 2
    THIRD = 3

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
    infl: list[Grammar] = field(default_factory=list)
    text: str = None
    page: str = None # ascii version of word
    meter: str = "" # meter of word
    pos: str = None # part of speech
    head: str = None # actual headword
    
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
    
    
#default grammar value for each pos
grammar_from_pos = {
    "pn": Noun(),
    "n": Noun(),
    "v": Verb(),
    "adj": Adjective(),
    }


    
word = Word() #the current word



def write_parsed(word):
    global output_lines
    if (word.text is None):
        return
    if (word.pos is None):
        return
    for infl in word.infl:
            output_lines.append (",".join((word.text, word.meter, word.pos, str(infl))))
            print (output_lines[-1])

def read_template(line):
    #pull out text
    possible_text = re.match("{{(.*)}}", line)
    if (possible_text is None):
        return None
    text = possible_text.group(1)
    #split on |
    parts = text.split('|')
    #name is 0
    print(parts[0])
    template = Template(parts[0])
    for i in (range(1, len(parts))):
        part = (parts[i])
        if ('=' in part):
            #labeled in dict by name
            (key, value) = part.split('=', 1)
            template.params[key] = value
        else:
            #unlabeled go in args
            template.args.append(part)
    return template

def template_head(word, template):
    if (len(template.args) > 1):
        pos = template.args[1]
        if (pos not in pos_from_head):
            return word
        word.pos = pos_from_head[pos]
    if ('head' in template.params):
        if (word.head is not None):
            write_parsed(word)
        word.text = template.params['head']
        word.meter = scanner.scan_text(word.text)
        word.head = word.text
    return word

def template_infl_of(word, template):
    #get set of grammars
    sets = []
    set = []
    for arg in template.args[3:]:
        if (arg == ";"): #move to a new set
            sets.append(set)
            set = []
        else:
            #deal with values
            values = arg.split("//")
            features = []
            for value in values:
                feature = string_to_feature(value)
                if (feature is not None):
                    features.append(feature)
            if (len(features) > 0):
                set.append(features)
    #store all sets and write each combination to a word
    sets.append(set)
    for set in sets:
        if (word.pos in grammar_from_pos):
            grammar = grammar_from_pos[word.pos]
            set_to_infls(word, set, grammar)
    return word

#recursive
def set_to_infls(word, set, grammar, index = 0):
    if (len(set) > index):
        #do something
        features = set[index]
        for feature in features:
            grammar = copy.deepcopy(grammar)
            grammar.set_feature(feature)
            set_to_infls(word, set, grammar, index + 1)
    else:
        #add grammar to word
        word.infl.append(grammar)
    pass

    
def parse_template(word, line):
    template = read_template(line)
    if (template is None):
        return word
    match (template.name):
        case "head":
            word = template_head(word, template)
        case "infl of" | "inflection of":
            word = template_infl_of(word,template)
    return word

def parse_heading(word, line):
    heading = line.replace('=', '')
    if (heading in pos_headings):
        word.pos = pos_headings[heading]
    return word
    
def parse_line(line):
    line = line.strip()
    global word
    if (line.startswith('=Lemma:=')):
        #print(word)
        write_parsed(word)
        text = line.removeprefix('=Lemma:=')
        word = Word(page=text, text=text)
        word.meter = scanner.scan_text(text)
    if ("{{" in line):
        word = parse_template(word, line)
    if (line.startswith("===")):
        word = parse_heading(word, line)

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
    

#read content
with open(filename) as file:
    for line in file:
        linecount += 1
        if (maxlines > 0 and linecount > maxlines):
            sys.exit(0)
        parse_line(line)
            

#write output

                    
                    
