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
            return (self.current[:-2] + combinations[junction] + meter [2:])

    """
    returns true is the new_current value is okay for the goal
    """
    def check_meter(self, meter):
        index = 0
        for f in range(len(self.goal)):
            foot = self.goal[f]
            #does this foot fit?
            foot_ok = False
            for o in foot.options:
                #print (meter[index:])
                if (meter[index:].startswith(o) or o.startswith(meter[index:-2])):
                    #print ("Yes", meter, index, o)
                    foot_ok = True
                    index += len(o)
                    break
            if (not(foot_ok)):
                return False
        return True

                
