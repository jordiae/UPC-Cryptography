#!/usr/bin/python3

from Crypto.Cipher import AES
import hashlib
m = hashlib.sha256()
#key_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

with open('2018_09_22_11_10_09_jordi.armengol.estape.puerta_trasera.enc','rb') as f:
	enc = f.read()
	
i = 0
n = 128#len(key_alphabet)
while i < n:
	j = 0
	while j < n:
		#si = key_alphabet[i]
		#sj = key_alphabet[j]
		#print(si)
		#print(sj)
		#print(si + si + si + si + si + si + si + si + sj + sj + sj + sj + sj + sj + sj + sj)
		#bits_i = ''.join([str(i) for n in bin(i)[2:].zfill(8)])# * 8
		#bits_j = ''.join([str(j) for n in bin(j)[2:].zfill(8)])# * 8
		#pmk = key_alphabet[i]*8 + key_alphabet[j]*8
		pmk = bytes([i])*8 + bytes([j])*8
		print(pmk)
		#pmk = (bits_i + bits_j).encode('ascii')
		#pmk = int(pmk, 2)
		#print(pmk)
		#preMasterKey = str((si + si + si + si + si + si + si + si + sj + sj + sj + sj + sj + sj + sj + sj).encode('ascii'))
		#print(preMasterKey)
		#H = hashlib.sha256(pmk.encode('ascii')).digest()#hexdigest()
		H = hashlib.sha256(pmk).digest()#hexdigest()
		
		#print(type(H))
		key = H[:16]
		iv = H[-16:] # initial vector
		cipher = AES.new(key,AES.MODE_CBC,iv)
		plaintext = cipher.decrypt(enc)#[AES.block_size:])
		correct_padding = True
		for path in range(1,plaintext[-1]):
			if plaintext[-1*path] != plaintext[-1]:
				correct_padding = False
				break
		if not correct_padding:
			j+= 1
			continue
		#if plaintext[-1] != plaintext[-2] or plaintext[-2] != plaintext[-3]:
		#	j += 1
		#	continue
		with open(str(i) + "_" + str(j),'wb') as fo:
			fo.write(plaintext)
		j += 1
	i += 1


#iv = enc[:AES.block_size] # initial vector
#cipher = AES.new(key,AES.MODE_CBC,iv)
#plaintext = cipher.decrypt(enc[AES.block_size:])
#with open('2018_09_22_11_10_09_jordi.armengol.estape.puerta_trasera.dec','wb') as fo:
#	fo.write(plaintext)
# # -*- coding: utf-8 -*-
