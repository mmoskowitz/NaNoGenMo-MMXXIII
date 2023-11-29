#!/usr/bin/env python3

import sys,re, copy
import scanner
import data

filename = sys.argv[1]

linecount = 0
maxlines = -1 #32000
debug = False

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

base_noun_store = {}

    
word = data.Word() #the current word

last_priority = 0
#priorities:
#0|=Lemma
#1|==Latin==
#2|===Pos===
#3|{{head,
#4|{{la-IPA
#5|{{la-*
#6|{{infl

def conditional_write_parsed(priority, word):
    global last_priority
    #print (priority, last_priority)
    if (priority <= last_priority):
        #print ("write", word)
        write_parsed(word)
    last_priority = priority
    

def write_parsed(word):
    global output_lines

    #skip some
    if (word.text is None):
        return
    if (word.pos is None):
        return
    if (len(word.meter) < 3):
        return
    if (re.search('^[a-zA-Z]+$', word.page) is None):
        return
    if (word.meter in ("VLV", "VSV", "VLM", "VSM")):
        return

    #what do we need for now?
    for infl in word.infl:
            output_lines.append (str_infl(word, infl))
            if (debug):
                print (output_lines[-1])

def str_infl(word, infl):
    return (",".join((word.text, word.meter, word.pos, str(infl))))
            
def read_template(line):
    #pull out text
    possible_text = re.match("{{(.*)}}", line)
    if (possible_text is None):
        return None
    text = possible_text.group(1)
    #split on |
    parts = text.split('|')
    #name is 0
    template = data.Template(parts[0])
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
        conditional_write_parsed(3, word)
        word.pos = pos_from_head[pos]
    if ('head' in template.params):
        word.text = template.params['head']
    else:
        word.text = word.page
    word.meter = scanner.scan_text(word.text)
    word.head = word.text
    return word

def template_la_IPA(word, template):
    if (len(template.args) > 0):
        conditional_write_parsed(4, word)
        head =  template.args[0]
        word.text = head
        word.meter = scanner.scan_text(word.text)
        word.head = word.text
    return word

def template_la_pos(word, template, pos=None):
    if (pos is None):
        pos = template.name[3:]
    if (pos not in data.grammar_from_pos):
        return word
    conditional_write_parsed(5, word)
    word.pos = pos
    word.infl = [copy.deepcopy(data.pos_to_grammar(word.pos))]
    if (len(template.args) > 0):
        head =  template.args[0]
        if (pos == "v"):
            head = template.args[1]
            if (head.endswith("t")): #impersonal verbs
                word.infl[0].set_feature("3")
        head_regex = "[^{0}]*([{0}]+)([^&]*&lt;([^&]*))?".format(scanner.letters) #move to const
        #print (head_regex)
        head_match = re.match(head_regex, head)
        if (head_match is None): #should not happen
            #print ("no match? no match!")
            return word
        head = head_match.group(1)
        code = head_match.group(3)
        if (head == "irreg"):
            return word
        word.text = head
        word.meter = scanner.scan_text(word.text)
        word.head = word.text
        if ("g" in template.params):
            word.infl[0].set_feature(template.params["g"])
        elif (code is not None):
            gender = gender_from_code(head, code)
            word.infl[0].set_feature(gender)
        if (isinstance(word.infl[0], data.Noun)):
            base_noun_store[head] = word.infl[0]
    return word

def gender_from_code(head, code):
    if (".M" in code):
        return "m"
    if (".F" in code):
        return "f"
    if (".N" in code):
        return "n"
    match(code[0]):
        case "1":
            if (head[-1] == "a" or head.endswith("ae")):
                return "f"
        case "2":
            if (head[-1] in "sr"):
                return "m"
            if (head[-1] in "mn"):
                return "n"
        case "3":
            if (head[-1] in ("oōx")):
                return "f"
            if (head[-1] in ("anel")):
                return "n"
            if (head[-1] == "s"):
                if (head[-2] == "o"):
                    return "m"
                if (head[-2] in "ua"):
                    return "n"
        case "4":
            if (head[-1] == "s"):
                return "m"
            else:
                return "n"
        case "5":
            return "f"
    return "NIHIL"
        

def template_infl_of(word, template):
    if (template.args[1] == "sum"): #forms of sum are too tricky
        word.page = "0"
        return word
    conditional_write_parsed(6, word)
    word.infl = []
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
                feature = data.string_to_feature(value)
                if (feature is not None):
                    features.append(feature)
            if (len(features) > 0):
                set.append(features)
    #store all sets and write each combination to a word
    sets.append(set)
    for set in sets:
        grammar = None
        if (word.pos in data.grammar_from_pos):
            grammar = data.grammar_from_pos[word.pos]
        if (isinstance(grammar, data.Noun)):
            if (template.args[1] in base_noun_store):
                grammar = base_noun_store[template.args[1]]
        if (grammar is not None):
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
        case "la-IPA":
            word = template_la_IPA(word, template)
        case "la-adj" | "la-adj-comp" | "la-adj-sup" | "la-det" | "la-num-adj" | "la-part":
            word = template_la_pos(word, template, "adj")
        case "la-adv" | "la-adv-comp" | "la-adv-sup" | "la-num-adv":
            word = template_la_pos(word, template, "adv")
        case "la-conj":
            word = template_la_pos(word, template, "conj")
        case "la-interj":
            word = template_la_pos(word, template, "intj")
        case "la-decl-gerund" | "la-gerund" | "la-noun" | "la-num-noun" | "la-praenomen" | "la-prop" | "la-proper noun" | "la-proper_noun":
            word = template_la_pos(word, template, "n")
        case "la-verb" :
            word = template_la_pos(word, template, "v")
        case "la-letter" | "la-phrase" | "la-prep" | "la-pronoun" :
            word = template_la_pos(word, template)
        case _:
            if (debug):
                print (template.name + " not parsed")
    return word

def parse_heading(word, line):
    heading = line.replace('=', '')
    if (heading in pos_headings):
        conditional_write_parsed(2, word)
        #word.text = word.page
        #word.head = word.page
        word.pos = pos_headings[heading]
        word.infl = [copy.deepcopy(data.pos_to_grammar(word.pos))]
    return word

def parse_line(line):
    line = line.strip()
    global word
    if (line.startswith('=Lemma:=')):
        #print(word)
        conditional_write_parsed(0, word)
        text = line.removeprefix('=Lemma:=')
        word = data.Word(page=text, text=text)
        word.meter = scanner.scan_text(text)
    if ("{{" in line):
        word = parse_template(word, line)
    if (line.startswith("===")):
        word = parse_heading(word, line)


#read content
with open(filename) as file:
    for line in file:
        linecount += 1
        if (maxlines > 0 and linecount > maxlines):
            for line in output_lines:
                print (line)
            sys.exit(0)
        parse_line(line)

    conditional_write_parsed(0, word)
            

#write output
for line in output_lines:
    print (line)
