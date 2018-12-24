#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from Crypto.PublicKey.RSA import importKey, construct, RSA # es pot fer servir from Crypto.PublicKey import RSA ? crec que no
import hashlib
import random
import sys

#from math import log

#from sympy import randprime, isprime
import sympy

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
			if sympy.gcd(phi_p,self.publicExponent) != 1:
				continue
			phi_q = self.primeQ - 1
			if sympy.gcd(phi_q,self.publicExponent) != 1:
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
		print("init")
	def sign(self,message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR
		'''
		print("sign")
		m1 = pow(m,int(self.privateExponentModulusPhiP),self.primeP)
		m2 = pow(m,int(self.privateExponentModulusPhiQ),self.primeQ)
		#hh = (self.privateExponentModulusPhiP - self.privateExponentModulusPhiQ)*self.inverseQModulusP % self.primeP
		hh = (m1 - m2) *self.inverseQModulusP % self.primeP
		return (self.privateExponentModulusPhiQ + self.primeQ*hh) # % self.modulus
	def sign_slow(self,message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR
		'''
		print("sign slow")
		s = pow(message,int(self.privateExponent),self.modulus)
		return s

r = rsa_key()
m = 324983253295
rs = r.sign(m)
rss = r.sign_slow(m) 
print(rs)
print(rss)
print(rs == rss)