
# This file was *autogenerated* from the file ../../Universitat/7/c/lab1_2/script_hill.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_7 = Integer(7); _sage_const_6 = Integer(6); _sage_const_5 = Integer(5); _sage_const_4 = Integer(4); _sage_const_9 = Integer(9); _sage_const_8 = Integer(8); _sage_const_13 = Integer(13); _sage_const_10 = Integer(10); _sage_const_16 = Integer(16); _sage_const_15 = Integer(15); _sage_const_14 = Integer(14); _sage_const_22 = Integer(22); _sage_const_19 = Integer(19); _sage_const_21 = Integer(21); _sage_const_26 = Integer(26); _sage_const_24 = Integer(24)# Frequency: THE = ATJ, AND = FYQ, ING = NDG
R = Integers(_sage_const_26 )
M = Matrix(R,[[_sage_const_19 ,_sage_const_7 ,_sage_const_4 ],[_sage_const_0 ,_sage_const_13 ,_sage_const_3 ],[_sage_const_8 ,_sage_const_13 ,_sage_const_6 ]]) # THE, AND, ING

A = Matrix(R,[[_sage_const_0 ],[_sage_const_5 ],[_sage_const_13 ]]) # A F N
B = Matrix(R,[[_sage_const_19 ],[_sage_const_24 ],[_sage_const_3 ]]) # T Y D
C = Matrix(R,[[_sage_const_9 ],[_sage_const_16 ],[_sage_const_6 ]]) # J Q G

K1 = M**(-_sage_const_1 )*A
K2 = M**(-_sage_const_1 )*B
K3 = M**(-_sage_const_1 )*C
K1 = transpose(K1)
K2 = transpose(K2)
K3 = transpose(K3)
K1
K2
K3

with open('/home/jordiae/Universitat/7/c/lab1_2/2018_09_10_12_57_30_jordi.armengol.estape.Hill', 'r') as myfile:
      encrypted_text =  AlphabeticStrings().encoding(myfile.read())

MS = MatrixSpace(R,_sage_const_3 ,_sage_const_3 )
K = MS([[_sage_const_15 ,_sage_const_19 ,_sage_const_6 ],[_sage_const_22 ,_sage_const_9 ,_sage_const_21 ],[_sage_const_13 ,_sage_const_10 ,_sage_const_14 ]])
K = transpose(K)


S = AlphabeticStrings()
H = HillCryptosystem(S,_sage_const_3 )

#print(H.deciphering(K,encrypted_text)[0:100])
with open("/home/jordiae/Universitat/7/c/lab1_2/out_hill_file.txt", "w") as text_file:
        text_file.write(str(H.deciphering(K,encrypted_text)))

