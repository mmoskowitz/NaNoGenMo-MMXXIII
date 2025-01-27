#!/usr/bin/env python3

import sys,re


checkflag = False
maxlines = 20
linecount = 0
allcount = 0

maxlinelength = 85

skipstarts = [
    '====',
    '===Abbreviations',
    '===Alternative',
    '===Anagrams',
    '===Circumfix',
    '===Contraction',
    '===Declension',
    '===Derived',
    '===Descend',
    '===Description',
    '===Diacritic',
    '===Etymology',
    '===Further',
    '===Letter',
    '===Notes',
    '===Paronyms',
    '===Particle', #could be used
    '===Phrase',
    '===Prefix',
    '===Pronunc',
    '===Proverb',
    '===Punctuation',
    '===References',
    '===Related',
    '===See also',
    '===Suffix',
    '===Symbol',
    '===Usage',
    'From ',
    '{|',
    '{{Currency symbols',
    '{{Latin personal',
    '{{PIE word',
    '{{adverbial accusative',
    '{{af',
    '{{anchor',
    '{{/table',
    '{{audio',
    '{{attention',
    '{{attn',
    '{{back-formation',
    '{{blend',
    '{{bl}}',
    '{{bottom',
    '{{c|',
    '{{cat|',
    '{{catlangcode',
    '{{catlangname',
    '{{circumfixsee',
    '{{cln',
    '{{col-',
    '{{col|',
    '{{col1',
    '{{col2',
    '{{col3',
    '{{col4',
    '{{col5',
    '{{collapse',
    '{{com+',
    '{{commonscat',
    '{{confix',
    '{{der2',
    '{{der3',
    '{{dercat',
    '{{des-',
    '{{diacritic',
    '{{elements',
    '{{etymid',
    '{{etystub',
    '{{compound',
    '{{con',
    '{{enum',
    '{{hcol',
    '{{la-correlatives',
    '{{la-decl-ppron',
    '{{la-ndecl',
    '{{la-timeline',
    '{{learned ',
    '{{lit',
    '{{multiple images',
    '{{nav-',
    '{{nbsp',
    '{{nonlemma',
    '{{nl',
    '{{phrasebook',
    '{{pre|',
    '{{prefix',
    '{{reduplication',
    '{{reflist',
    '{{rel-',
    '{{rel2',
    '{{rel3',
    '{{rel4',
    '{{rfap',
    '{{rfd',
    '{{rfe',
    '{{rfi',
    '{{rfinfl',
    '{{rfref',
    '{{rfc',
    '{{rfv',
    '{{semantic loan',
    '{{slim-wikipedia',
    '{{swp|',
    '{{sl|',
    '{{sup|',
    '{{suf',
    '{{table:',
    '{{tea room',
    '{{top2',
    '{{top3',
    '{{top4',
    '{{top5',
    '{{topics',
    '{{ubor',
    '{{unc|',
    '{{univ|',
    '{{univerbation',
    '{{unk|',
    '{{unknown',
    '{{VL',
    '{{was ',
    '{{wiki',
    '{{word|',
    '{{wp',
    '{{ws',
]
skipconts = [
    '{{...}}',
    '{{&amp;lit',
    '{{+preo',
    '{{AD',
    '{{C|',
    '{{CE',
    '{{IPA',
    '{{Latin letter',
    '{{Latn-def',
    '{{Q|',
    '{{P:',
    '{{R:',
    '{{RQ:',
    '{{U:',
    '{{a|',
    '{{abbr',
    '{{afex',
    '{{affix',
    '{{also',
    '{{alt form',
    '{{alternative',
    '{{alter|',
    '{{altform',
    '{{alti',
    '{{alt|',
    '{{alt sp',
    '{{altsp',
    '{{anagrams',
    '{ant|',
    '{antonyms',
    '{{archaic',
    '{{audio',
    '{{bor',
    '{{c|',
    '{{cal|',
    '{{calque',
    '{{circa',
    '{{cite',
    '{{cln',
    '{{clipping',
    '{{clq',
    '{{cog',
    '{{coi',
    '{{com|',
    '{{comd of',
    '{{comparative',
    '{{contraction',
    '{{contr of',
    '{{coord',
    '{{cot',
    '{{def-see',
    '{{def-uncertain',
    '{{der',
    '{{dhub',
    '{{dim of',
    '{{diminutive',
    '{{desc',
    '{{ellipsis',
    '{{femeq',
    '{{female equiv',
    '{{feminine ',
    '{{frequentative of',
    '{{gerund of',
    '{{gloss',
    '{{gl|',
    '{{historical',
    '{{hmp',
    '{{hol|',
    '{{holo',
    '{{homophone',
    '{{hyp-',
    '{{hyph',
    '{{hyper',
    '{{hypo',
    '{{i|',
    '{{inh',
    '{{init of',
    '{{initialism',
    '{{ja-r',
    '{{ja-l',
    '{{l-lite',
    '{{la-adecl',
    '{{la-epithet',
    '{{la-ipa',
    '{{la-ndecl',
    '{{la-praenom',
    '{{lang',
    '{{label',
    '{{lbor',
    '{{lb|',
    '{{lbl',
    '{{link',
    '{{list',
    '{{l|',
    '{{m+|',
    '{{m|',
    '{{m-lite',
    '{{m-self',
    '{{medieval',
    '{{mero',
    '{{missp',
    '{{n-g',
    '{{ng',
    '{{non-gloss',
    '{{number box',
    '{{obsolete',
    '{{onomatopoeic',
    '{{par',
    '{{partial calque',
    '{{pedia',
    '{{place',
    '{{plural of',
    '{{prefixusex',
    '{{present participle',
    '{{q-lite',
    '{{qual|',
    '{{qualifier',
    '{{quote',
    '{{q|',
    '{{rare ',
    '{{rel adj',
    '{{rfdate',
    '{{rfdef',
    '{{rhymes',
    '{{rfq',
    '{{rfv',
    '{{root',
    '{{scrib',
    '{{see ',
    '{{see|',
    '{{seeCites',
    '{{seemoreCites',
    '{{sense',
    '{{short for',
    '{{singular of',
    '{{smallcaps',
    '{{superlative',
    '{{surname',
    '{{syn',
    '{{s|',
    '{{t|',
    '{{t+|',
    '{{taxlink',
    '{{tlb',
    '{{term-label',
    '{{top',
    '{{tr',
    '{{transclude',
    '{{ux',
    '{{usex',
    '{{vern',
    '{{w|',
    '{{→',
    ' stem===',
    ' spelling of|'
]
keepstarts = [
    '===Adjective',
    '===Adverb',
    '===Article',
    '===Conjunction',
    '===Determiner',
    '===Idiom',
    '===Interjection',
    '===Gerund',
    '===Noun',
    '===Numeral',
    '===Participle',
    '===Postposition',
    '===Preposition',
    '===Pronoun',
    '===Proper noun',
    '===Verb',
    '==Latin==',
    '{{g|',
    '{{head',
    '{{la-adj',
    '{{la-adv',
    '{{la-conj',
    '{{la-det',
    '{{la-decl-gerund',
    '{{la-gerund',
    '{{la-interj',
    '{{la-letter',
    '{{la-noun',
    '{{la-num-adj',
    '{{la-num-adv',
    '{{la-num-noun',
    '{{la-part',
    '{{la-phrase',
    '{{la-prep',
    '{{la-pronoun',
    '{{la-prop',
    '{{la-verb',
    
]
keepconts = [
    '=Lemma',
    '{{form_of',
    '{{la-IPA',
    '{{la-noun',
    '{{inflection',
    '{{infl of',
    '{{given name',
    '{{la-praenomen',
    '{{alt case',
    'form of|',
]

filename = sys.argv[1]

#check a line, return -1 (skip), 1 (keep), or 0 (not def)
def checkline(line):
    if (len(line) > maxlinelength):
        return -1
    for start in keepstarts:
        if (line.startswith(start)):
            return 1
    for cont in keepconts:
        if (cont in line):
            return 1
    if (not(checkflag)):
        return -1
    for start in skipstarts:
        if (line.startswith(start)):
            return -1
    for cont in skipconts:
        if (cont in line):
            return -1
    if (line[0] not in '={*#'):
        return -1
    if (re.search('[\*#] [\w\[\']', line)): #start of text
        return -1
    return 0
    

#read content
with open(filename) as file:
    for line in file:
        allcount += 1
        if ('{' not in line and '=' not in line):
            continue
        action = checkline(line)
        if (action < 0):
            #don't write to file
            continue
        if (action > 0):
            #write to file
            if (not(checkflag)):
                print (line)
            continue
        if (checkflag): #unhandled
            linecount += 1
            if (linecount > maxlines):
                print ("position: " + str(allcount))
                sys.exit(0)
            print (line)
