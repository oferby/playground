import numpy as np

B = np.matrix([[1, 3, 4], [2, 4, 0], [3, 1, 1]])


A = np.matrix([[2, 1, 2], [4, 0, 3], [0, 3, 5]])
temp = A
print("A:")
print(A)

E1 = np.matrix([[1, 0, 0], [-2, 1, 0], [0, 0, 1]])
temp = E1 * A
print("E1:")
print(temp)

E2 = np.matrix([[1, 0, 0], [0, 1, 0], [0, 1, 1]])
temp = E2 * temp
print("E2:")
print(temp)

E3 = np.matrix([[1, 0, -1], [0, 1, 2], [0, 0, 1]])
temp = E3 * temp
print("E3:")
print(temp)

E4 = np.matrix([[0.5, 0, 0], [0, 1 / 7, 0], [0, 0, 1]])
temp = E4 * temp
print("E4:")
print(temp)

E5 = np.matrix([[1, 1, 0], [0, 1, 0], [0, -4, 1]])
temp = E5 * temp
print("E5:")
print(temp)

E6 = np.matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
temp = E6 * temp
print("E6:")
print(temp)

print("B:")
print(B)

E = B * E6 * E5 * E4 * E3 * E2 * E1
print("E:")
print(E)
print("E * A:")
print(E * A)
