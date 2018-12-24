#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
with open('2018_09_22_11_10_09_jordi.armengol.estape.key','rb') as f1:
	key = f1.read()
with open('2018_09_22_11_10_09_jordi.armengol.estape.enc','rb') as f2:
	enc = f2.read()
	

#key = open("2018_09_22_11_10_09_jordi.armengol.estape.key").read()
#enc = open("2018_09_22_11_10_09_jordi.armengol.estape.enc").read()
iv = enc[:AES.block_size] # initial vector
cipher = AES.new(key,AES.MODE_CFB,iv)
plaintext = cipher.decrypt(enc[AES.block_size:])
with open('2018_09_22_11_10_09_jordi.armengol.estape.dec','wb') as f2:
	f2.write(plaintext)
#open('2018_09_22_11_10_09_jordi.armengol.estape.dec','wb').write(plaintext)

