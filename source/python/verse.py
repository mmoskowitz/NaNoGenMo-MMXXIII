#!/usr/bin/env python3

from dataclasses import dataclass, field
import data

combinations = {
    "LMVL": "L",
    "LMVS": "L",
    "LMCL": "LL",
    "LMCS": "LS",
    "LMXL": "LL",
    "LMXS": "LS",
    "LVVL": "L",
    "LVVS": "L",
    "LVCL": "LL",
    "LVCS": "LS",
    "LVXL": "LL",
    "LVXS": "LS",
    "LCVL": "LL",
    "LCVS": "LS",
    "LCCL": "LL",
    "LCCS": "LS",
    "LCXL": "LL",
    "LCXS": "LS",
    "LXVL": "LL",
    "LXVS": "LS",
    "LXCL": "LL",
    "LXCS": "LS",
    "LXXL": "LL",
    "LXXS": "LS",
    "SMVL": "L",
    "SMVS": "S",
    "SMCL": "SL",
    "SMCS": "LS",
    "SMXL": "LL",
    "SMXS": "LS",
    "SVVL": "L",
    "SVVS": "S",
    "SVCL": "SL",
    "SVCS": "SS",
    "SVXL": "LL",
    "SVXS": "LS",
    "SCVL": "SL",
    "SCVS": "SS",
    "SCCL": "LL",
    "SCCS": "LS",
    "SCXL": "LL",
    "SCXS": "LS",
    "SXVL": "LL", #SX should never occur
    "SXVS": "LS",
    "SXCL": "LL",
    "SXCS": "LS",
    "SXXL": "LL",
    "SXXS": "LL",
}

"""
options must be composed of L and S
"""
@dataclass
class Foot:
    options: list[str] = field(default_factory=list)

@dataclass
class Verse:
    goal: list[Foot] = field(default_factory=list)
    current: str = ""
    words: list[str] = field(default_factory=list)

    def add_word(self, word):
        self.current = self.get_new_current(word.meter)
        self.words.append(word.head)


    def __str__(self):
        return (self.current[:-1] + ": " + " ".join(self.words))

    def get_new_current(self, meter):
        #TODO: check the new meter vs. the goal        
        if (len(self.current) == 0):
            return (self.current + meter[1:])
        else:
            junction = self.current[-2:] + meter[:2]
            #print (junction, combinations[junction])
            return (self.current[:-2] + combinations[junction] + meter [2:])

    """
    returns true is the meter value is okay for the goal
    """
    def check_meter(self, meter, check_complete=False):
        index = 0
        for foot in self.goal:
            #does this foot fit?
            foot_ok = False
            for o in foot.options:
                #print (meter[index:])
                if (
                    meter[index:].startswith(o) or
                    (o.endswith("L") and o.startswith(meter[index:-2])) or
                    (o.endswith("S") and o.startswith(meter[index:-1]))
                ):
                    foot_ok = True
                    index += len(o)
                    #print ("Yes", meter, index, o)
                    break
            if (not(foot_ok)):
                return False
            elif (index == len(meter) - 1): #complete
                if (check_complete and foot != self.goal[-1]):
                    return False
                return True

        if (index < len(meter) - 1): #verse too long
            return False
        if (check_complete): #check for full verse or not
            return False
        else:
            return True

    def get_next_meters(self, lexicon):
        current = self.current
        meters = []
        if (self.check_meter(current, True)):
            return []
        #dumb brute force as initial implementation
        for meter in lexicon.meters:
            possible_current = self.get_new_current(meter)
            if (self.check_meter(possible_current)):
                meters.append(meter)
        return meters
