#!/usr/bin/env python3

import sys,re

filename = sys.argv[1]

title = ''

output_lines = []
is_text = False
is_latin = False

#read content
with open(filename) as file:
    for line in file:
        if (is_text):
            if (is_latin):
                if (re.match('^==[^=]+==.*', line)):
                    is_latin = False
                    break
                elif (line.find("</text") >= 0):
                    output_lines.append(line[0:line.find("</text")])
                    break
                      
                else:
                    output_lines.append(line)
            else:
                if (line.startswith('==Latin==')):
                    is_latin=True
                    output_lines.append(line)
                    
        else: # is not text
            match = re.search("<title>(.*)</title>", line)
            if (match is not None):
                title = match.group(1)
            elif (line.find("<text ") >= 0): #start text
                is_text = True
                if (line.find("==Latin==") >= 0):
                    is_latin=True
                    output_lines.append("==Latin==")

filename_id = filename.split('/')[-1][:-4]
with open(title.replace(' ', '_') + filename_id + ".txt", "w") as output:
    output.write("=Lemma:=" + title + "\n")
    for line in output_lines:
        output.write(line)
                    
                    
    

            
