#!/usr/bin/python3

import AESPython
import matplotlib.pyplot as plt
import numpy as np
import functools

def set_bit(v, index, x):
  """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
  mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
  v &= ~mask          # Clear the bit indicated by the mask (if x is False)
  if x:
    v |= mask         # If x was True, set the bit indicated by the mask.
  return v            # Return the result, we're done.

def get_bit(n, k):
	k = k + 1
	print(n," ",k)
	print()
	if n & (1 << (k - 1)):
		return 1
	else:
		return 0

def count_set_bits( n ): 
    count = 0
    while n > 0: 
        count += n & 1
        n >>= 1
    return count 

def get_number_bits_changed(a,b):
	different_bits_mask = a ^ b
	return count_set_bits(different_bits_mask)

def get_which_bits_changed(a,b):
	different_bits_mask = a ^ b
	bf = bitfield(different_bits_mask)
	i = 0
	changed_positions = []
	while i < len(bf):
		if bf[i] == 1:
			changed_positions.append(i)
		i += 1
	return changed_positions


def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

K = 0x2b7e151628aed2a6abf7158809cf4f3c
aes = AESPython.AES(K)
M = 0x15337eb3971c6deac4c21b3bef8b2e95
C = aes.encrypt(M)
number_bits_changed = []
#number_bits_changed = {}
# BITS QUE CANVIEN
i = 0
while i < 128:
	bit = get_bit(M,i)
	Mi = M
	if bit == 1:
		Mi = set_bit(M,i,0)
	else:
		Mi = set_bit(M,i,1)
	Ci = aes.encrypt(Mi)
	number_bits_changed.append(get_number_bits_changed(C,Ci))
	#number_bits_changed[i] = get_number_bits_changed(C,Ci)
	i += 1

for x in number_bits_changed:
	print(x)

hist, bin_edges = np.histogram(number_bits_changed)

i = 0
x_axis = []
while i < 128:
	x_axis.append(i)
	i += 1


l = number_bits_changed
print(functools.reduce(lambda x, y: x + y, l) / len(l))

# An "interface" to matplotlib.axes.Axes.hist() method

n, bins, patches = plt.hist(x=x_axis, bins=list(range(0, 127)), color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis=number_bits_changed, alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('My Very Own Histogram')
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.savefig('hola.jpg')


fig, ax = plt.subplots()
ax.bar(x_axis, number_bits_changed, width = 0.8, align="center")
plt.xlabel('# changed bits')
plt.ylabel('# apperances')
plt.show()
#plt.savefig('./out/hist1.png')#, bbox_inches='tight')
plt.close(fig)

#l = number_bits_changed
#print(reduce(lambda x, y: x + y, l) / len(l))





# POSICIONS QUE CANVIEN


K = 0x2b7e151628aed2a6abf7158809cf4f3c
aes = AESPython.AES(K)
M = 0x15337eb3971c6deac4c21b3bef8b2e95
C = aes.encrypt(M)
bits_changed = {}
#number_bits_changed = {}
# BITS QUE CANVIEN
i = 0
while i < 128:
	bit = get_bit(M,i)
	Mi = M
	if bit == 1:
		Mi = set_bit(M,i,0)
	else:
		Mi = set_bit(M,i,1)
	Ci = aes.encrypt(Mi)
	positions_changed = get_which_bits_changed(C,Ci)
	for x in positions_changed:
		if x in bits_changed:
			bits_changed[x] += 1
		else:
			bits_changed[x] = 1
	#number_bits_changed[i] = get_number_bits_changed(C,Ci)
	i += 1

for x in number_bits_changed:
	print(x)

hist, bin_edges = np.histogram(number_bits_changed)

i = 0
x_axis = []
while i < 128:
	x_axis.append(i)
	i += 1


#l = number_bits_changed
print(functools.reduce(lambda x, y: x + y, l) / len(l))

# An "interface" to matplotlib.axes.Axes.hist() method

n, bins, patches = plt.hist(x=x_axis, bins=list(range(0, 127)), color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis=number_bits_changed, alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('My Very Own Histogram')
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.savefig('hola.jpg')

bits_changed_list = []
i = 0
while i < 128:
	bits_changed_list.append(bits_changed[i])
	i += 1


fig, ax = plt.subplots()
ax.bar(x_axis, bits_changed_list, width = 0.8, align="center")
plt.xlabel('# changed bits')
plt.ylabel('# apperances')
plt.show()
plt.savefig('./out/hist1.png')#, bbox_inches='tight')
plt.close(fig)






"""

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
"""