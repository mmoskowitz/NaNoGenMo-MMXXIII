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

@dataclass
class Verse:
    goal: str = ""
    current: str = ""
    words: list[str] = field(default_factory=list)

    def add_word(self, word):
        if (len(self.current) == 0):
            self.current = self.current + word.meter[1:]
        else:
            junction = self.current[-2:] + word.meter[:2]
            print (junction)
            self.current = self.current[:-2] + combinations[junction] + word.meter [2:]
            
        self.words.append(word.head)


    def __str__(self):
        return (self.current[:-1] + ": " + " ".join(self.words))
