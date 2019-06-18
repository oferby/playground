# use Matrices to compute probability
import numpy as np

A = np.diag([0.2, 0.7, 0.1])
BA = np.matrix([[0.3, 0.5, 0.2], [0.4, 0.4, 0.2]])

l1 = np.matrix([1, 0, 0])  # a0
l2 = np.matrix([0, 1])  # b1
l3 = np.matrix([0, 1, 0])  # c1

print('a0:', A[0][0])
print('b1 a0: ', l1 * A * BA.transpose() * l2.transpose())

AandB = A * BA.transpose()
print('\nb joint a:\n', AandB)
print('\nb joint a:\n', AandB.flatten())

CgivenB = np.matrix([[0.4, 0.6], [0.55, 0.45], [0.1, 0.9]])

CandA = A * BA.transpose() * CgivenB.transpose()
print('\nc joint a:\n', CandA) # a0 c1
print('\nc joint a:\n', CandA[1,0]) # c1,a0
print('\nc1 a0: ', l3 * A * BA.transpose() * CgivenB.transpose() * l1.transpose()) # a0 c1
print('\nc1 b1: ', [0, 1] * CgivenB.transpose() * l3.transpose()) # b1 c1


print('\nRKHS: ', np.dot(l2,  BA * l1.transpose())) # < A1, CbaB2 >



