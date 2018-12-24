#!/usr/bin/python3
# -*- coding: utf-8 -*-

import timeit

exponencial = [None] * 256 # No necessari 256 -> 255
logaritme = [None] * 256 # No necessari 256 -> 255

def GF_product_p(a,b):
	""" Entrada: a i b elements del cos representat per enters entre 0 i 255;
		Sortida: un element del cos representat per un enter entre 0 i 255 que
		es el producte en el cos de a i b fent servir la definicio en termes
		de polinomis """

	nbits = 8 # (0-255)
	i = 0
	result = 0
	#m = 0x1B # x^4 + x^3 + x + 1, irreductible (no falta x^8?)
	#m = 0x9B # x^8 + x^4 + x^3 + x + 1 = 1 0 0 0 1 1 0 1 1 = 0x11B
	#m = 0x1B
	m = 0x11B
	while i < nbits:
		# print(i);
		if b & 0x01 == 1: # Si el bit menys significant de b es 1
			result = (result ^ a)##%256#%m#256 # xor
		# print(hex(a));
		#a = (a << 1)#%256# % 256# shift tan si el bit mes significant es 0 o 1
		#print(hex(a));
		#print("msb = " + hex(a) + " & 0x80 " + " = " + hex(a & 0x80))
		if a & 0x80 == 0x80: # Si el bit mes signifcant de a es 1
		    a = (a << 1)
		    #print(hex(a));
		    a = (a ^ m)%256 #% 256 # xor
		else:
			a = (a << 1)
		#print(hex(a));
		b = b >> 1
		i = i + 1
	return result

	# https://crypto.stackexchange.com/questions/21173/how-to-calculate-aes-logarithm-table

def GF_tables():
	""" Entrada:
		Sortida: dues taules (exponencial i logaritme), una que a la posicio i
		tingui a = g**i (g = 0x03), i una altra que a la posicio a tingui i tal
		que a = g**i """
	#exponencial = [None] * 256 # No necessari 256 -> 255
	#logaritme = [None] * 256 # No necessari 256 -> 255
	n = 255
	k = 1
	g = 0x03
	exponencial[0] = 1
	logaritme[0] = 0
	while k <= 255:
		i = k
		#a = (g**i) % 256
		a = GF_product_p(exponencial[i-1],g)
		exponencial[i] = a
	
		logaritme[a] = i
		k = k + 1
	logaritme[1] = 0
	#l = list(map(hex,exponencial))
	#print(l)
	logaritme[0] = None


def GF_product_t(a,b):
	""" Entrada: a i b elements del cos representat per enters entre 0 i 255 
		Sortida: un element del cos representat per un enter entre 0 i 255 que
		és el producte en el cos de a i b fent servir les taules exponencial i
		logaritme """
	# es podria fer restant 255 si es mes gran de 255
	# o tambe: modul 255 sempre
	#return exponencial[(logaritme[a] + logaritme[b])%255]
	x1 = logaritme[a]
	x2 = logaritme[b]
	if x1 == None:
		x1 = 0
	if x2 == None:
		x2 = 0
	x = x1 + x2
	if x > 255:
		return exponencial[x - 255]
	else:
		return exponencial[x]

def gcd(a,b):
	""" Aux gcd """
	if a == 0:
		return b
	return gcd(b % a, a)


def GF_generador():
	""" Dona tots els generadors del cos finit """
	i = 0
	generadors = [] # n'hi hauria d'haver phi(k) = 128 (k = 256)
	while i < 256:
		# si g es generador, els altres son g^k tal que mod(k,255)=1
		g_candidate = exponencial[i]
		k = 255
		if gcd(i,k) == 1:
			generadors.append(g_candidate)
		i = i + 1
	generadors.sort()
	#l = list(map(hex,generadors))
	#print(l)
	#print(len(l))
	return None

def GF_invers(a):
	""" Entrada: a element del cos representat per un enter entre 0 i 255
	que es el producte en el cos de a i b fent servir les taules exponencial i
	logaritme """
	result = a
	if result != 0:
		# Inversos: 0x05 es a la posicio 1 -> el seu invers el trobem a 255 - 1
		pos = logaritme[a]
		result = exponencial[255-pos]

	return result

"""def aux_taules_comparatives(b,f):
	a = 0
	# timeit
	while a < 256:
		f(a,b)
		a += 1"""
def run_GF_product_p(b):
	a = 0
	while a < 256:
		GF_product_p(a,b)
		a += 1

def run_GF_product_t(b,preload_tables):
	if not preload_tables:
		GF_tables()
	a = 0
	while a < 256:
		GF_product_t(a,b)
		a += 1

def taules_comparatives():
	# GF_product_p vs GF_product_t

	print("Preloading tables for GF_product_t")
	print()
	print()
	# GF_product_p(a,0x02) vs GF_product_t(a,0x02)
	"""a = 0
	# timeit
	while a < 256:
		GF_product_p(a,0x03)
		a += 1

	GF_tables()
	a = 0
	# timeit
	while a < 256:
		GF_product_t(a,0x03)
		a += 1
	"""
	b = 0x02
	GF_tables()
	#t1 = timeit.timeit(aux_taules_comparatives(b,GF_product_p))
	#t2 = timeit.timeit(aux_taules_comparatives(b,GF_product_t))
	t1 =  timeit.timeit('run_GF_product_p(0x02)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x02,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x02) vs GF_product_t(a,0x02)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()

	# GF_product_p(a,0x03) vs GF_product_t(a,0x03)
	t1 =  timeit.timeit('run_GF_product_p(0x03)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x03,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x03) vs GF_product_t(a,0x03)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()
	# GF_product_p(a,0x09) vs GF_product_t(a,0x09)

	t1 =  timeit.timeit('run_GF_product_p(0x09)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x09,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x09) vs GF_product_t(a,0x09)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()


	# GF_product_p(a,0x0B) vs GF_product_t(a,0x0B)

	t1 =  timeit.timeit('run_GF_product_p(0x0B)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0B,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0B) vs GF_product_t(a,0x0B)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()


	# GF_product_p(a,0x0D) vs GF_product_t(a,0x0D)

	t1 =  timeit.timeit('run_GF_product_p(0x0D)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0D,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0D) vs GF_product_t(a,0x0D)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()

	# GF_product_p(a,0x0E) vs GF_product_t(a,0x0E)

	t1 =  timeit.timeit('run_GF_product_p(0x0E)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0E,True)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0E) vs GF_product_t(a,0x0E)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()
	print()
	print()
	print()
	
	print("Without preloading tables for GF_product_t")
	print()
	print()






	t1 =  timeit.timeit('run_GF_product_p(0x02)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x02,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x02) vs GF_product_t(a,0x02)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()

	# GF_product_p(a,0x03) vs GF_product_t(a,0x03)
	t1 =  timeit.timeit('run_GF_product_p(0x03)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x03,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x03) vs GF_product_t(a,0x03)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()
	# GF_product_p(a,0x09) vs GF_product_t(a,0x09)

	t1 =  timeit.timeit('run_GF_product_p(0x09)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x09,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x09) vs GF_product_t(a,0x09)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()


	# GF_product_p(a,0x0B) vs GF_product_t(a,0x0B)

	t1 =  timeit.timeit('run_GF_product_p(0x0B)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0B,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0B) vs GF_product_t(a,0x0B)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()


	# GF_product_p(a,0x0D) vs GF_product_t(a,0x0D)

	t1 =  timeit.timeit('run_GF_product_p(0x0D)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0D,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0D) vs GF_product_t(a,0x0D")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()

	# GF_product_p(a,0x0E) vs GF_product_t(a,0x0E)

	t1 =  timeit.timeit('run_GF_product_p(0x0E)', 'from __main__ import run_GF_product_p',number=10)
	t2 =  timeit.timeit('run_GF_product_t(0x0E,False)', 'from __main__ import run_GF_product_t',number=10)
	print("GF_product_p(a,0x0E) vs GF_product_t(a,0x0E)")
	print("Without tables: ", t1)
	print("With tables:    ", t2)
	print()











GF_tables()
x = hex(GF_product_t(0x38,0xe4))
print(x) # 0x3c
x = hex(GF_product_t(0xd3,0x26))
print(x) # 0xf9
GF_generador()
x = hex(GF_invers(0x05))
print(x) # 0x52

taules_comparatives()