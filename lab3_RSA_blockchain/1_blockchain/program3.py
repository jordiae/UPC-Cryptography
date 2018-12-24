#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sympy
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
		return (m2 + self.primeQ*hh) # % self.modulus
	def sign_slow(self,message):
		'''
		retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR
		'''
		print("sign slow")
		s = pow(message,int(self.privateExponent),self.modulus)
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
		s = pow(signature, int(self.publicExponent), self.modulus)
		m = message % self.modulus
		return s == m