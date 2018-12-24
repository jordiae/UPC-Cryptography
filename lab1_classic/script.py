#!/usr/bin/python3
# -*- coding: utf-8 -*-

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def break_scyla():
    with open('2018_09_10_12_57_30_jordi.armengol.estape.Escitalo', 'r') as myfile:
      cypher_bom = myfile.read()
      cypher = '\ufeff' + cypher_bom[6:]
    print(len(cypher))
    r = 149
    decypher = ''
    i = 0
    while i < r:
        j = i
        while j < len(cypher):
            decypher += cypher[j]
            j = j + r
        i = i + 1
    with open("out.txt", "w") as text_file:
        text_file.write(decypher)

def main():
    #break_scyla()
    #exit()
    with open('2018_09_10_12_57_30_jordi.armengol.estape.Escitalo', 'r') as myfile:
      cypher_bom = myfile.read()
      cypher = '\ufeff' + cypher_bom[6:]
    r = 1
    while r < len(cypher):
        print(str(r) + ' of ' + str(len(cypher)))
        decypher = ''
        i = 0
        while i < r:
           j = i
           while j < len(cypher):
               decypher += cypher[j]
               j = j + r
           i = i + 1
        if decypher.count(" the ") > 100:
            print(r)
            print(decypher[0:200])
            #print(decypher)
        r = r + 1
    
main()
