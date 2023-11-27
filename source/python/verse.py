#!/usr/bin/env python3

from dataclasses import dataclass, field
import re
import data

combinations = {
    "LMVL": "L",
    "LMVS": "L",
    "LMCL": "L L",
    "LMCS": "L S",
    "LMXL": "L L",
    "LMXS": "L S",
    "LVVL": "L",
    "LVVS": "L",
    "LVCL": "L L",
    "LVCS": "L S",
    "LVXL": "L L",
    "LVXS": "L S",
    "LCVL": "L L",
    "LCVS": "L S",
    "LCCL": "L L",
    "LCCS": "L S",
    "LCXL": "L L",
    "LCXS": "L S",
    "LXVL": "L L",
    "LXVS": "L S",
    "LXCL": "L L",
    "LXCS": "L S",
    "LXXL": "L L",
    "LXXS": "L S",
    "SMVL": "L",
    "SMVS": "S",
    "SMCL": "L L",
    "SMCS": "L S",
    "SMXL": "L L",
    "SMXS": "L S",
    "SVVL": "L",
    "SVVS": "S",
    "SVCL": "S L",
    "SVCS": "S S",
    "SVXL": "L L",
    "SVXS": "L S",
    "SCVL": "S L",
    "SCVS": "S S",
    "SCCL": "L L",
    "SCCS": "L S",
    "SCXL": "L L",
    "SCXS": "L S",
    "SXVL": "L L", #SX should never occur
    "SXVS": "L S",
    "SXCL": "L L",
    "SXCS": "L S",
    "SXXL": "L L",
    "SXXS": "L L",
}

"""
options must be composed of L and S
"""
@dataclass
class Foot:
    options: list[str] = field(default_factory=list)
    caesura: bool = False #primus || ab oris: caes on "primus ab"
    diaeresis: bool = False # conderet / urbem: diae on "conderet"

    def __str__(self):
        return (
            ("/".join(self.options))
            + ("(c)" if self.caesura else "")
            + ("(d)" if self.diaeresis else "")
        )

@dataclass
class Verse:
    goal: list[Foot] = field(default_factory=list)
    current: str = ""
    words: list[str] = field(default_factory=list)
    debug: bool = False

    def add_word(self, word):
        self.current = self.get_new_current(word.meter)
        self.words.append(word.head)


    def __str__(self):
        return (" ".join(self.words))

    def get_new_current(self, new_meter):
        #TODO: check the new meter vs. the goal        
        if (len(self.current) == 0):
            return (self.current + new_meter[1:])
        elif (len(new_meter) == 0):
            return self.current
        else:
            junction = self.current[-2:] + new_meter[:2]
            #print (junction, combinations[junction])
            return (self.current[:-2] + combinations[junction] + new_meter [2:])

    """
    returns true if the meter value is okay for the goal
    """
    def check_meter(self, new_meter, check_complete=False):
        meter = self.get_new_current(new_meter) #this is current with meter added
        index = 0
        for foot in self.goal:
            if (len(meter) == 0 and check_complete):
                return False
            if (
                    index + 3 > len(meter) and
                    len(meter) > 0 and
                    not(check_complete)
            ):
                return True
            
            foot_check = self.check_foot(index, foot, meter, new_meter, check_complete)
            if (foot_check < 0):
                return False
            else:
                index = foot_check
        #all feet used
        if (index < len(meter) - 1): #verse too long
            return False
        return True

    """
    checks an individual foot and returns the new index or -1 if failed
    """
    def check_foot(self, index, foot, meter, new_meter, check_complete=False):
        #does this foot fit?
        foot_ok = False
        meter_from_index = meter[index:]
        pure_meter_from_index = meter_from_index.replace(" ", "")
        for o in foot.options:
            if (pure_meter_from_index.startswith(o)): #basic meter ok
                real_foot_regex = " ?" + " ?".join(o)
                real_foot_match = re.match(real_foot_regex, meter_from_index)
                if (foot.caesura):
                    caesura_regex = " ?({})".format(" ?".join(o))
                    caesura_match = re.match(caesura_regex, meter_from_index)
                    if (caesura_match is None or len(caesura_match.group(1)) == len(o)):
                        #no break at beginning of foot
                        continue
                if (foot.diaeresis):
                    if (not(meter_from_index.startswith(" "))):
                        #no break before word
                        continue
                foot_ok = True
                if (real_foot_match is None):
                    index += len(meter_from_index)
                else:
                    index_update =  len(real_foot_match.group(0))
                    index += index_update
                break
            elif (
                    (o.endswith("L") and o.startswith(pure_meter_from_index[:-2])) or
                    (o.endswith("S") and o.startswith(pure_meter_from_index[:-1]))
            ):
                real_foot_regex = " ?" + " ?".join(pure_meter_from_index[:-1])
                real_foot_match = re.match(real_foot_regex, meter_from_index)
                #caesura automatically ok if meter ends mid-foot
                if (foot.diaeresis):
                    if (not(meter_from_index.startswith(" "))):
                        #no break before word
                        continue
                foot_ok = True
                if (real_foot_regex is None):
                    index += len(meter_from_index)
                else:
                    index_update =  len(real_foot_match.group(0))
                    index += index_update
                break
                    
        if (not(foot_ok)): 
            return -1
        elif (index == len(meter) - 1): #complete
            if (check_complete and foot != self.goal[-1]):
                return -1
            else:
                return index
        return index
            
    
        
    def get_next_meters(self, lexicon):
        temp_meters = []
        if (self.check_meter("", True)):
            return []
        #dumb brute force as initial implementation
        for new_meter in lexicon.meters:
            #print ("checking possible ", new_meter)
            if (self.check_meter(new_meter)):
               temp_meters.append(new_meter)
        return temp_meters
