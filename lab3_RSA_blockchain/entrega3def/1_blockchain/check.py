#!/usr/bin/python3
# -*- coding: utf-8 -*-

import blockchain
import random
import sys
import timeit
import pickle

fitxer_de_sortida = '100_blocks_valids.block'
with open(fitxer_de_sortida, 'rb') as file:
		cadena_de_blocs = pickle.load(file)
print(cadena_de_blocs.verify())