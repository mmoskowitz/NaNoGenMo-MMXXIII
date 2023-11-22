#!/usr/bin/env python3

import sys,re, copy
import scanner
import data

filename = sys.argv[1]

meters = {}

def parse_line(line):
    global meters
    parts = line.split(',')
    (head, meter, pos) = parts[0:3]
    word = data.Word(head, pos, meter)
    if (meter not in meters):
        meters[meter] = []
    meters[meter].append(head)
    #print (word, meter, len(meters[meter]))


#read content
with open(filename) as file:
    for line in file:
        parse_line(line)


for meter in meters:
    print (len(meters[meter]), meter)


