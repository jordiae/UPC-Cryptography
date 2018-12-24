with open("raw/certificate_subjectPublicKey.bin", "rb") as f:
	certificate = f.read()


Px = int(certificate[1:((len(certificate) - 1)//2 + 1)].encode('hex'),16)
Py = int(certificate[((len(certificate) - 1)//2 + 1):2*(((len(certificate) - 1)//2)+1)].encode('hex'),16)
print(Px)
print(Py)
