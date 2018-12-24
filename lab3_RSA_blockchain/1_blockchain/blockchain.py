#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sympy
import hashlib
import sys
import random


class rsa_key:
	def __init__(self, bits_modulo=2048, e=2**16 + 1):
		'''
		genera una clau RSA (de 2048 bits i amb exponent públic 2**16+1 per defecte)
		'''
		self.publicExponent = e
		correct_primes = False
		while not correct_primes:
			self.primeP = sympy.randprime(
			    2**(bits_modulo // 2 - 1), 2**(bits_modulo // 2) - 1)
			self.primeQ = sympy.randprime(
			    2**(bits_modulo // 2 - 1), 2**(bits_modulo // 2) - 1)
			phi_p = self.primeP - 1
			if sympy.gcd(phi_p, self.publicExponent) != 1:
				continue
			phi_q = self.primeQ - 1
			if sympy.gcd(phi_q, self.publicExponent) != 1:
				continue
			correct_primes = True
		phi_n = (self.primeP - 1) * (self.primeQ - 1)
		# lcm = phi_p * phi_q / math.gcd(phi_p,phi_q)
		lcm = sympy.lcm(phi_p, phi_q)
		self.privateExponent = sympy.invert(self.publicExponent, lcm)
		self.modulus = self.primeP * self.primeQ
		self.privateExponentModulusPhiP = self.privateExponent % phi_p
		self.privateExponentModulusPhiQ = self.privateExponent % phi_q
		self.inverseQModulusP = sympy.invert(self.primeQ, self.primeP)

	def sign(self, message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR
		'''
		m1 = pow(message, int(self.privateExponentModulusPhiP), self.primeP)
		m2 = pow(message, int(self.privateExponentModulusPhiQ), self.primeQ)
		h = (m1 - m2) * self.inverseQModulusP % self.primeP
		#print("hola")
		#return h
		return (m2 + self.primeQ * h)

	def sign_slow(self, message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR
		'''
		s = pow(message, int(self.privateExponent), self.modulus)
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
		s = pow(int(signature), self.publicExponent, self.modulus)
		m = message % self.modulus
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
		return self.public_key.verify(self.message, self.signature)


class block:
	def __init__(self):
		'''
		crea un bloc (no necessàriament vàlid)
		'''
		self.block_hash = None
		self.previous_block_hash = None
		self.transaction = None
		self.seed = None
		self.d = 8

	def genesis(self, transaction):
		'''
		genera el primer bloc d’una cadena amb la transacció "transaction" que es caracteritza per:
		- previous_block_hash=0
		- ser vàlid
		'''
		self.previous_block_hash = 0
		self.transaction = transaction
		self.calc_set_block_hash()

	def next_block(self, transaction):
		'''
		genera el següent block vàlid amb la transacció "transaction"
		'''
		new_block = block()
		new_block.transaction = transaction
		new_block.previous_block_hash = self.block_hash
		new_block.calc_set_block_hash()
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
		if self.previous_block_hash >= 2**(256-self.d):
			return False
		if not self.transaction.verify():
			return False
		if self.block_hash >= 2**(256-self.d):
			return False
		return True

	def is_genesis(self):
		return self.previous_block_hash == 0 and self.verify_block()

	def calc_set_block_hash(self):
		self.seed = random.randint(0,sys.maxsize)
		entrada = str(self.previous_block_hash)
		entrada = entrada+str(self.transaction.public_key.publicExponent)
		entrada = entrada+str(self.transaction.public_key.modulus)
		entrada = entrada+str(self.transaction.message)
		entrada = entrada+str(self.transaction.signature)
		entrada = entrada+str(self.seed)
		h = int(hashlib.sha256(entrada.encode()).hexdigest(),16)
		while h >= 2**(256-self.d):
			self.seed = random.randint(0,sys.maxsize)
			entrada = str(self.previous_block_hash)
			entrada = entrada+str(self.transaction.public_key.publicExponent)
			entrada = entrada+str(self.transaction.public_key.modulus)
			entrada = entrada+str(self.transaction.message)
			entrada = entrada+str(self.transaction.signature)
			entrada = entrada+str(self.seed)
			h = int(hashlib.sha256(entrada.encode()).hexdigest(),16)
		self.block_hash = h


class block_chain:
	def __init__(self,transaction):
		'''
		genera una cadena de blocs que és una llista de blocs,
		el primer bloc és un bloc "genesis" generat amb la transacció "transaction"
		'''
		b = block()
		b.genesis(transaction)
		self.list_of_blocks = [b]
	def add_block(self,transaction):
		'''
		afegeix a la llista de blocs un nou bloc vàlid generat amb la transacció "transaction"
		'''
		self.list_of_blocks.append(self.list_of_blocks[-1].next_block(transaction))

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