import sympy, hashlib

# b) 

# p-256
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
generador = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
Gx = generador[0]
Gy = generador[1]
print("b): Ordre primer?")
print(n in Primes())


# c)

#pubKey = '0x04fdc06b1e5673e346198eaa48b37b13bf0b2c79b2059e1c707c97b7726da48b8223d232de50231c3dba6d2b7178f5028bb0840de136553ae4e504ad6e7a6e87df'
#P = (0xfdc06b1e5673e346198eaa48b37b13bf0b2c79b2059e1c707c97b7726da48b82,0x23d232de50231c3dba6d2b7178f5028bb0840de136553ae4e504ad6e7a6e87df)

with open("raw/certificate_subjectPublicKey.bin", "rb") as f:
	certificate = f.read()

#certificate = hex(0x04FDC06B1E5673E346198EAA48B37B13BF0B2C79B2059E1C707C97B7726DA48B8223D232DE50231C3DBA6D2B7178F5028BB0840DE136553AE4E504AD6E7A6E87DF)


Px = int(certificate[1:((len(certificate) - 1)//2 + 1)].encode('hex'),16)
Py = int(certificate[((len(certificate) - 1)//2 + 1):2*(((len(certificate) - 1)//2)+1)].encode('hex'),16)






print("c): El punt forma part de la corba si en compleix l'equacio (obtenim 0):")
print(mod(Py**2,p)-mod(Px**3+a*Px+b,p))



# d)
Zp = Zmod(p)
E = EllipticCurve(Zp,[a,b]);
P = E([Px,Py])
print("d) L'ordre de la corba es:")
print(P.order())


# e)


with open("raw/server_key_exchange_signature.bin", "rb") as f:
         signature = f.read()
f1 = int(signature[4:36].encode('hex'),16)
f2 = int(signature[38:70].encode('hex'),16)






with open("raw/client_hello_random.bin","rb") as f:
	m = f.read()
with open("raw/server_hello_random.bin","rb") as f:
	m += f.read()
with open("raw/server_key_exchange_curve_type.bin","rb") as f:
	m += f.read()
with open("raw/server_key_exchange_named_curve.bin","rb") as f:
	m += f.read()
with open("raw/server_key_exchange_pubkey_length.bin","rb") as f:
	m += f.read()
with open("raw/server_key_exchange_pubkey.bin","rb") as f:
	m += f.read()


hashed = hashlib.sha512(m).hexdigest()
hashed = hashed[:64]
hashed = int(hashed,16)
inv2 = sympy.invert(f2,n)
w1 = int((hashed*inv2)%n)
w2 = int((f1*inv2)%n)
P = E([Gx,Gy])
Q = E([Px,Py])
P_ = w1*P + w2*Q
print("e) Verificar la firma:")
print(f1 == int(P_[0])%n)