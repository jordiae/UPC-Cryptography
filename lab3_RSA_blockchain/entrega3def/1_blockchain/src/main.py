#!/usr/bin/python3
# -*- coding: utf-8 -*-
import blockchain
import random
import sys
import timeit
import pickle

def taula_comparativa_signar():
	"""
	Una taula comparativa amb el temps necessari per signar, fent servir el TXR i sense fer-ho servir, 100
	missatges diferents amb claus de 512, 1024, 2048 i 4096 bits.
	"""
	key_sizes = [512,1024,2048,4096]
	size_message = 2**20
	times_sign = [0]*len(key_sizes)
	times_sign_slow = [0]*len(key_sizes)
	messages = []
	for i in range(0,100):
		print(i)
		m = random.randint(2**(size_message // 2 - 1), 2**(size_message // 2) - 1)
		messages.append(m)
		for j,key_size in enumerate(key_sizes):
			t_sign =  timeit.timeit('rsa.sign(' + str(m) + ')','import blockchain; rsa = blockchain.rsa_key(' + str(key_size) + ');',number=3)
			t_sign_slow = timeit.timeit('rsa.sign_slow(' + str(m) + ')','import blockchain; rsa = blockchain.rsa_key(' + str(key_size) + ');',number=3)
			times_sign[j] += t_sign
			times_sign_slow[j] += t_sign_slow
	print('Taula comparativa signar amb TXR vs no TXR, 100 missatges diferents, amb m diferents, ' + str(size_message))
	print('TXR Key_size time')
	for i,t in enumerate(times_sign):
		print('SI ' + str(key_sizes[i]) + ' ' + str(t))
	for i,t in enumerate(times_sign_slow):
		print('NO' + str(key_sizes[i]) + ' ' + str(t))

def fitxer_100_blocs_valids():
	"""Un fitxer amb una cadena vàlida de 100 blocs"""
	rsa_0 = blockchain.rsa_key()
	m_0 = random.randint(0,sys.maxsize)
	t_0 = blockchain.transaction(m_0,rsa_0)
	cadena_de_blocs = blockchain.block_chain(t_0)
	for i in range (1,100):
		print(i)
		rsa = blockchain.rsa_key()
		m = random.randint(0,sys.maxsize)
		t = blockchain.transaction(m,rsa)
		cadena_de_blocs.add_block(t)
	print(cadena_de_blocs.verify())
	fitxer_de_sortida = '100_blocks_valids.block'
	with open(fitxer_de_sortida, 'wb') as file:
		pickle.dump(cadena_de_blocs, file)

def fitxer_100_blocs_valids_fins_XX_DNI():
	"""
	Un fitxer amb una cadena de 100 blocs que només sigui vàlida fins al bloc XX on XX són les dues darreres
	xifres del vostre DNI.
	"""
	XX_DNI = 81 # ara mateix NO INCLÒS EN ELS VÀLIDS
	rsa_0 = blockchain.rsa_key()
	m_0 = random.randint(0,sys.maxsize)
	t_0 = blockchain.transaction(m_0,rsa_0)
	cadena_de_blocs = blockchain.block_chain(t_0)
	for i in range (1,XX_DNI):
		print(i)
		rsa = blockchain.rsa_key()
		m = random.randint(0,sys.maxsize)
		t = blockchain.transaction(m,rsa)
		cadena_de_blocs.add_block(t)
	print(cadena_de_blocs.verify())
	for i in range (XX_DNI,100):
		print(i)
		rsa = blockchain.rsa_key()
		m = random.randint(0,sys.maxsize)
		t = blockchain.transaction(m,rsa)
		t.signature = random.randint(0,sys.maxsize) # fem que sigui invàlida la transacció, també podríem alterar el hash etc
		# Nota: en tindríem prou amb alterar-ne un de sol (el 81) perquè els següents també fossin invàlids, es trenca la cadena
		cadena_de_blocs.add_block(t)
	print(cadena_de_blocs.verify())
	fitxer_de_sortida = '81_blocks_valids.block'
	with open(fitxer_de_sortida, 'wb') as file:
		pickle.dump(cadena_de_blocs, file)

def main():
	taula_comparativa_signar()
	#fitxer_100_blocs_valids()
	#fitxer_100_blocs_valids_fins_XX_DNI()

if __name__ == "__main__":
    main()