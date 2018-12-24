import random, sympy, hashlib
# a) 
# p-256
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
generador = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
Gx = generador[0]
Gy = generador[1]


Zp = Zmod(p)
E = EllipticCurve(Zp,[a,b]);
G = E([Gx,Gy])
#r = random.randint(1,n)
r = 32903829104380230318795649424761085390545183133709242454697246715961201857515
print("Clau privada (r) = " + str(r))
public_key = r*G
print("Clau publica (r*G) = " + str(public_key))



# b) 

# Firmar amb la nostra:
m1 = b"Cryptography is easy"
m2 = b"Fake news!"
hash_m1 = hashlib.sha256(m1).hexdigest()
hash_m2 = hashlib.sha256(m2).hexdigest()
k = 2019
kinv = sympy.invert(k,n)
punt = k*public_key
kinv = sympy.invert(k,n)
f1_m1 = int(punt[0]) % n
f2_m1 = kinv * (int(hash_m1,16) + f1_m1 * r) % n
f1_m2 = int(punt[0]) % n
f2_m2 = kinv * (int(hash_m2,16) + f1_m2 * r) % n

print("sha256 m1 = " + hash_m1)
print("firma m1 = " + str(f1_m1) + ", " + str(f2_m1))
print("sha256 m2 = " + hash_m2)
print("firma m2 = " + str(f1_m2) + ", " + str(f2_m2))

# Descobrir la clau privada d'un company

Qx,Qy = (92676570939053145599593557428948850941030526200314965959660924601076446593629, 6999937258047710598380608891850485412069804973684303062788491443880259738713)
Q = E([Qx,Qy])

print("Clau publica (Q) = " + str(Q))

hash_msg1 = 0x1af8a350161756100593aa0534e82ba3bbced07e0d2795d8dfaf0b74a9720f35
f1_msg1, f2_msg1 = (56515219790691171413109057904011688695424810155802929973526481321309856242040, 88768016934213900963631164825481081219684706718533808043657779770914320630189)

hash_msg2 = 0xeaa75c66efe2f4e56aa472c64053848e810d5003d6530a80ee5d8717b800fd31
f1_msg2, f2_msg2= (56515219790691171413109057904011688695424810155802929973526481321309856242040, 19944661966426200242090262633833485915724471099137845157073108624329285538650)


sinv = sympy.invert((f2_msg1 - f2_msg2) % n, n)
rinv = sympy.invert(f1_msg1, n)
k = int(sinv*(hash_msg1 - hash_msg2) % n)
r_company = int(rinv*(k*f2_msg1 - hash_msg1) % n)

print("Nombre aleatori (k) = " + str(k))
print("Clau privada (r_company) " + str(r_company))





"""
# Comprovacio amb la meva propia firma i missatges
Q = public_key

print("Clau publica (Q) = " + str(Q))

hash_msg1 = 0xfa2c69f5aab9536f791dc66344ed56180011c3f5aa51073f74679266c8dc58bc
f1_msg1, f2_msg1 = (57639030199670191689327471105980108676024191299351505593390738464915115528888, 97817915981740604817533758315828502753053076692623323008325544761698153163039)

hash_msg2 = 0x143db322cfd3f19479667fef72d708c77b4c91feee5592f9b83f2452678a05b2
f1_msg2, f2_msg2= (57639030199670191689327471105980108676024191299351505593390738464915115528888, 42250435164824155873179808297112714501276069492567062193740563831235894853401)


sinv = sympy.invert((f2_msg1 - f2_msg2) % n, n)
rinv = sympy.invert(f1_msg1, n)
k = int(sinv*(hash_msg1 - hash_msg2) % n)
r_company = int(rinv*(k*f2_msg1 - hash_msg1) % n)

print("Nombre aleatori (k) = " + str(k))
print("Clau privada (r_company) " + str(r_company))

"""