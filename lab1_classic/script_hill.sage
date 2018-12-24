# Frequency: THE = ATJ, AND = FYQ, ING = NDG
R = Integers(26)
M = Matrix(R,[[19,7,4],[0,13,3],[8,13,6]]) # THE, AND, ING

A = Matrix(R,[[0],[5],[13]]) # A F N
B = Matrix(R,[[19],[24],[3]]) # T Y D
C = Matrix(R,[[9],[16],[6]]) # J Q G

K1 = M^(-1)*A
K2 = M^(-1)*B
K3 = M^(-1)*C
K1 = transpose(K1)
K2 = transpose(K2)
K3 = transpose(K3)
K1
K2
K3

with open('/home/jordiae/Universitat/7/c/lab1_2/2018_09_10_12_57_30_jordi.armengol.estape.Hill', 'r') as myfile:
      encrypted_text =  AlphabeticStrings().encoding(myfile.read())

MS = MatrixSpace(R,3,3)
K = MS([[15,19,6],[22,9,21],[13,10,14]])
K = transpose(K)


S = AlphabeticStrings()
H = HillCryptosystem(S,3)

#print(H.deciphering(K,encrypted_text)[0:100])
with open("/home/jordiae/Universitat/7/c/lab1_2/out_hill_file.txt", "w") as text_file:
        text_file.write(str(H.deciphering(K,encrypted_text)))
