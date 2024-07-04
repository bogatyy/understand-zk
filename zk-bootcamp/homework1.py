import numpy as np
import galois

PRIME = 71

# Define the field
Z_P = galois.GF(PRIME)

# Matrix stuff

A = Z_P([[52, 24, 61],
        [40, 40, 58],
        [1, 2, 3]])

A_inv = np.linalg.inv(A)

print("Matrix A:\n", A)
print("Inverse of A:\n", A_inv)
print("A * A_inv:\n", A @ A_inv)

# Polynomials

p = galois.Poly([52, 24, 61], field=Z_P)
q = galois.Poly([40, 40, 58], field=Z_P)

print("p(x) =", p)
print("q(x) =", q)
print("p(x) * q(x) =", p * q)

print("Roots of P, Q, P * Q in Z_P:", p.roots(), q.roots(), (p * q).roots())

# Interpolation

x = Z_P([0, 1, 2])
y = Z_P([1, 2, 1])

f = galois.lagrange_poly(x, y)
print("F", f)
for xx, yy in zip(x, y):
    print(xx, yy, f(xx))
