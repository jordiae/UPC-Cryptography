#!/usr/python3

from sys import argv
from fractions import gcd
from Crypto.PublicKey.RSA import importKey, construct
from glob import glob

keys_dir = "RSA_RW-20181109/"
user = "jordi.armengol.estape"
pub_key_ext = "_pubkeyRSA_RW.pem"


target_key = importKey(open(keys_dir + user + pub_key_ext).read())

p = 1
 
# Find common divisor with other keys
for filename in glob(keys_dir + '*pubkey*.pem'):
    if filename != keys_dir + user + pub_key_ext:
        candidate_key = importKey(open(filename).read())
        p = gcd(target_key.n, candidate_key.n)
 
    if p != 1:
        #print("primer amb",filename)
        break
 
q = target_key.n // p 
if p * q != target_key.n:
    raise "Error computing p and q"
 
euler_n = target_key.n - (p + q - 1)
 
def inverse(a, n):
    t = 0
    r = n
    newt = 1
    newr = a
 
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
 
    if r > 1:
        raise "a is not invertible"
 
    if t < 0:
        t = t + n
 
    return t

# Compute private exponent
d = inverse(target_key.e, euler_n)
 
# Generate private key
private_key = construct((target_key.n, target_key.e, d, p, q))
print(private_key.exportKey().decode('utf-8'))