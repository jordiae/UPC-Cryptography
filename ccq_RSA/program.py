#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sympy import invert

with open('xifratfinal.txt','r') as f:
	c = f.read()
c = c[:-1] # per eliminar caracter final \n
print("El missatge que tenim intencio de desencriptar es...")
print(c)
print()
# 1: factoritzar
n = 297045209
nn = n
factors = []
i = 2
while i <= nn and nn > 1:
	if nn % i == 0:
		factors.append(i)
		nn = nn / i
	i += 1
[p,q] = factors
print("Els factors de n = " + str(n) + " son p = " + str(p) + " i q = " + str(q))

# 2: obtenir clau privada
e = 31273
totient = (p-1)*(q-1)
k = invert(e,totient)
print("La clau privada es k = " + str(k))

# 3: Desencriptar C
l = 9
i = 0
dec = ""
while i < len(c):
	p_i = pow(int(c[i:i+l]),int(k),n) # exponenciacio modular rapida
	dec_i = str(p_i)
	while len(dec_i) < (l-1):
		dec_i = "0" + dec_i
	dec += dec_i
	i += l

if int(dec[0:3]) > 254:
	dec = "0" + dec

missatge = ""
i = 0
while i < len(dec):
	missatge += chr(int(dec[i:i+3]))
	i += 3
missatge = missatge[:-3] # sense treure els ultims caracters estem generant un fitxer invalid
print("El missatge desencriptat P es...")
print(missatge)

#4: Escriure missatge P
with open('text_desxifrat.txt', 'w') as f:
	f.write(missatge)