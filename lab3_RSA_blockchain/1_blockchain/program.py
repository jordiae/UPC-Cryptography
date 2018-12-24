#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Crypto.PublicKey.RSA import importKey, construct, RSA # es pot fer servir from Crypto.PublicKey import RSA ? crec que no
import hashlib
import random
import sys

from math import log

from sympy import randprime, isprime

#seed_range = range(0,sys.maxsize)
seed_range_a = 0
seed_range_b = sys.maxsize
#d = 8
"""
class block:
	def __init__(self):
		self.block_hash
		self.previous_block_hash
		self.transaction
		self.seed

class transaction:
	def __init__(self, message, RSAkey):
		self.public_key
		self.message
		self.signature

class rsa_key:
	def __init__(self,bits_modulo=2048, e =2**16+1):
		self.publicExponent
		self.privateExponent
		self.modulus
		self.primeP
		self.privateExponentModulusPhiP
		self.privateExponentModulusPhiQ
		self.inverseQModulusP

class rsa_public_key:
	def __init__(self, rsa_key):
		self.publicExponent
		self.modulus
"""

class rsa_key:
	def __init__(self,bits_modulo=2048,e=2**16+1):
		'''
		genera una clau RSA (de 2048 bits i amb exponent públic 2**16+1 per defecte)
		'''
		self.publicExponent = e
		correct_primes = False
		while not correct_primes:
			self.primeP = sympy.randprime(2**(bits_modulo//2-1),2**(bits_modulo//2)-1)
			self.primeQ = sympy.randprime(2**(bits_modulo//2-1),2**(bits_modulo//2)-1)
			phi_p = self.primeP - 1
			if sympy.gcd(phi_p,self.publicExponent) == 1:
				continue
			phi_q = self.primeQ - 1
			if sympy.gcd(phi_q,self.publicExponent) == 1:
				continue
			correct_primes = True
		phi_n = (self.primeP - 1) * (self.primeQ - 1)
		#lcm = phi_p * phi_q / math.gcd(phi_p,phi_q)
		lcm = sympy.lcm(phi_p,phi_q)
		self.privateExponent  = sympy.invert(self.publicExponent,lcm)
		self.modulus = self.primeP * self.primeQ
		self.privateExponentModulusPhiP = self.privateExponent % phi_p
		self.privateExponentModulusPhiQ = self.privateExponent % phi_q
		self.inverseQModulusP = sympy.invert(self.primeQ,self.primeP)

	def sign(self,message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR
		'''
		return ((privateExponentModulusPhiP - privateExponentModulusPhiQ) * inverseQModulusP) % modulus
	def sign_slow(self,message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR
		'''
		s = (message ** privateExponent) % modulus
		return s


class rsa_public_key:
	def __init__(self, rsa_key):
		'''
		genera la clau pública RSA asociada a la clau RSA "rsa_key"
		'''
		self.publicExponent = rsa_key.publicExponent
		self.modulus = rsa_key.modulus
	def verify(self, message, signature):
		'''
		retorna el booleà True si "signature" es correspon amb una
		signatura de "message" feta amb la clau RSA associada a la clau
		pública RSA.
		En qualsevol altre cas retorma el booleà False
		'''
		s = (signature ** publicExponent) % modulus
		m = message % modulus
		return s == m

class transaction:
	def __init__(self, message, RSAkey):
		'''
		genera una transacció signant "message" amb la clau "RSAkey"
		'''
		self.public_key = rsa_public_key(RSAkey)
		self.message = message
		self.signature = RSAkey.sign(message)
	def verify(self):
		'''
		retorna el booleà True si "signature" es correspon amb una
		signatura de "message" feta amb la clau pública "public_key".
		En qualsevol altre cas retorma el booleà False
		'''
		return self.public_key.verify(message,signature)


class block:
	def __init__(self):
		'''
		crea un bloc (no necessàriament vàlid)
		'''
		self.block_hash = None
		self.previous_block_hash = None
		self.transaction = None
		self.seed = None

	def genesis(self,transaction):
		'''
		genera el primer bloc d’una cadena amb la transacció "transaction" que es caracteritza per:
		- previous_block_hash=0
		- ser vàlid
		'''
		g = block()
		g.block_hash = 0
		g.previous_block_hash = None
		g.transaction = transaction
		g.seed = random.randint(seed_range_a,seed_range_b)
		return g
		#return block(block_hash = 0, previous_block_hash = None, self.transaction = transaction, self.seed = random.randint(seed_range_a,seed_range_b))
	def next_block(self, transaction):
		'''
		genera el següent block vàlid amb la transacció "transaction"
		'''
		new_block = block()
		new_block.transaction = transaction
		new_block.previous_block_hash = self.block_hash
		new_block.seed = self.seed
		new_block.block_hash = new_block.calc_block_hash()
		return new_block

	def verify_block(self):
		'''
		Verifica si un bloc és vàlid:
		-Comprova que el hash del bloc anterior cumpleix las condicions exigides
		-Comprova la transacció del bloc és vàlida
		-Comprova que el hash del bloc compleix las condicions exigides
		Si totes les comprovacions són correctes retorna el booleà True.
		En qualsevol altre cas retorma el booleà False
	    '''
	    d = 8
	    if self.previous_block_hash >= 2**(256-d):
	    	return False
	    if not self.transaction.verify():
	    	return False
	    if self.block_hash >= 2**(256-d):
	    	return False
	    return True

	def is_genesis(self):
		return self.previous_block_hash == 0 and self.verify_block()

	def calc_block_hash(self):

	    entrada=str(self.previous_block_hash)
		entrada=entrada+str(self.transaction.public_key.publicExponent)
		entrada=entrada+str(self.transaction.public_key.modulus)
		entrada=entrada+str(self.transaction.message)
		entrada=entrada+str(self.transaction.signature)
		entrada=entrada+str(self.seed)
		h=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
		return h
		


class block_chain:
	def __init__(self,transaction):
		'''
		genera una cadena de blocs que és una llista de blocs,
		el primer bloc és un bloc "genesis" generat amb la transacció "transaction"
		'''
		self.list_of_blocks = [block.genesis(transaction)]
	def add_block(self,transaction):
		'''
		afegeix a la llista de blocs un nou bloc vàlid generat amb la transacció "transaction"
		'''
		self.list_of_blocks.append(self.list_of_blocks[-1:].next_block(transaction))

	def verify(self):
		'''
		verifica si la cadena de blocs és vàlida:
		- Comprova que tots el blocs són vàlids
		- Comprova que el primer bloc és un bloc "genesis"
		- Comprova que per cada bloc de la cadena el següent és el correcte
		Si totes les comprovacions són correctes retorna el booleà True.
		En qualsevol altre cas retorna el booleà False i fins a quin bloc la cadena és vàlida
		'''
		if not self.list_of_blocks[0].is_genesis():
			return False
		for b in self.list_of_blocks[1:]:
			if not b.verify_block():
				return False
		return True



# D U B T E S



# BLOCKCHAIN:
# "- Comprova que per cada bloc de la cadena el següent és el correcte" ja es fa amb block.verify_block(), a l'igual que "Comprova que tots el blocs són vàlids"?


# BLOCK
# __init__ de block ho ha de deixar tot a None?
# Seed?
# A verify block, comprovar que el hash anterior i l'actual compleixin les condiciones exigides vol dir només que h < 2**(256-d) o també mirar que el hash sigui del block, i la transacció sigui correcta etc?


# fins aqui, dubtes meh. pero dubtes hardcore:

# RSA PUBLIC KEY
# Estic comprovant correctament la firma?


# RSA KEY
# Com genero tots els parametres? A saber:

"""self.publicExponent = e
		self.privateExponent
		self.modulus
		self.primeP
		self.primeQ
		self.privateExponentModulusPhiP
		self.privateExponentModulusPhiQ
		self.inverseQModulusP
"""

# Recomanacions per generar nombres random? Al document diu "veure documentacions mes endanvant", pero on son?
# Com signo rnormal vs slow?



#import pickle
#with open(fitxer_de_sortida, ’wb’) as file:
#pickle.dump(cadena_de_blocs, file)