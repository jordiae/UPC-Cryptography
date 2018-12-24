#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import sys
import hashlib
d = 8
x = int(hashlib.sha256(str(random.randint(0,sys.maxsize)).encode()).hexdigest(),16)
dd = 2**(256-d)
while  x >= dd:
	print(x)
	print(dd)
	print(dd >= x)
	y = int(hashlib.sha256(str(random.randint(0,sys.maxsize)).encode()).hexdigest(),16)
	print(y == x)
	print()
	x = y

print(x)
print(dd)
print(dd >= x)