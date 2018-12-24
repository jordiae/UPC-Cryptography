#!/usr/bin/python3

import AESPython
import AESPythonMixColumnsId




K = 0x2b7e151628aed2a6abf7158809cf4f3c

M = 0x15337eb3971c6deac4c21b3bef8b2e95
Mi = 0x15337eb3971c6deac4821b3bef8b2e95
Mj = 0x15337e93971c6deac4c21b3bef8b2e95
Mij = 0x15337e93971c6deac4821b3bef8b2e95

# AES OK

print("AES OK")

aes_ok = AESPython.AES(K)
C = aes_ok.encrypt(M)
Ci = aes_ok.encrypt(Mi)
Cj = aes_ok.encrypt(Mj)
Cij = aes_ok.encrypt(Mij)

R = Ci ^ Cj ^ Cij
print("C == Ci ^ Cj ^ Cij ?", C == R)
print("C = ",C)
print("Ci = ",Ci)


# AES MixColumns = Id

print("AES MixColumns = Id")

aes_mixcolumns_id = AESPythonMixColumnsId.AES(K)
C = aes_mixcolumns_id.encrypt(M)
Ci = aes_mixcolumns_id.encrypt(Mi)
Cj = aes_mixcolumns_id.encrypt(Mj)
Cij = aes_mixcolumns_id.encrypt(Mij)

R = Ci ^ Cj ^ Cij
print("C == Ci ^ Cj ^ Cij ?", C == R)
print("C = ",C)
print("Ci = ",Ci)
