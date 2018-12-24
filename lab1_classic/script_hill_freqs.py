#!/usr/bin/python3
# -*- coding: utf-8 -*-

def find_common_trigraphs(text):
  freqs = {}
  i = 0
  while i < len(text)-4:
    trigraph = text[i:i+3]
    if trigraph in freqs:
      freqs[trigraph] += 1
    else:
      freqs[trigraph] = 1
    i += 1
  return freqs

def main():
    with open('2018_09_10_12_57_30_jordi.armengol.estape.Hill', 'r') as myfile:
      cypher = myfile.read()
    freqs = find_common_trigraphs(cypher)
    ordered_freqs = []
    ordered_freqs_index = {}
    for dict_key, dict_value in freqs.items():
      #print(dict_key + ',' + str(freqs[dict_key]) + ';')
      ordered_freqs.append(dict_value)
      if not dict_value in ordered_freqs_index.items():
        ordered_freqs_index[dict_value] = [dict_key]
      else:
         ordered_freqs_index[dict_value].append(dict_key)

    ordered_freqs.sort()

    print(ordered_freqs_index[ordered_freqs[-1]],ordered_freqs[-1])
    print(ordered_freqs_index[ordered_freqs[-2]],ordered_freqs[-2])
    print(ordered_freqs_index[ordered_freqs[-3]],ordered_freqs[-3])
    print(ordered_freqs_index[ordered_freqs[-4]],ordered_freqs[-4])

    #['ATJ'] 3680
    #['FYQ'] 2364
    #['NDG'] 1759



    
main()
