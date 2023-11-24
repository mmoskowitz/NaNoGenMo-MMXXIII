#!/usr/bin/env python3

import random
import data

random.seed(2023)

"""
Needs:
* word by pos and meter(s)
* word by infl and meter
* verb by number and meter

Use the infl as the key, dummy
"""
class Lexicon():
    meters = {}
    infls = {data.Grammar()} 

    def parse_line(self, line):
        word = data.Word.parse_line(line)
        self.add_word(word)
    
    def add_word(self, word):
        meter = word.meter
        infl = word.infl[0]
        if (infl not in self.infls):
            self.infls.add(infl)
        if (meter not in self.meters):
            self.meters[meter] = {}
        meter_infls = self.meters[meter]
        if (infl not in meter_infls):
            meter_infls[infl] = []
        meter_infls[infl].append(word)

    def get_word(self, meters, infls=()):
        words = []
        for meter in meters:
            if (meter in self.meters):
                meter_infls = self.meters[meter]
                for infl in meter_infls:
                    for requested_infl in infls:
                        if (infl.matches(requested_infl)):
                            words.extend(meter_infls[infl])
        return random.choice(words)
        
