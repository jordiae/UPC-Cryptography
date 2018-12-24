#!/usr/bin/python3

import AESPython
import AESPythonByteSubId




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


# AES ByteSub = Id

print("AES ByteSub = Id")

aes_bytesub_id = AESPythonByteSubId.AES(K)
C = aes_bytesub_id.encrypt(M)
Ci = aes_bytesub_id.encrypt(Mi)
Cj = aes_bytesub_id.encrypt(Mj)
Cij = aes_bytesub_id.encrypt(Mij)

R = Ci ^ Cj ^ Cij
print("C == Ci ^ Cj ^ Cij ?", C == R)