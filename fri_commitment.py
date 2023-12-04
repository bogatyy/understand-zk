import random

from polynomial import Polynomial


MODULO = 10

# For learning purposes, easily verifiable > cryptographically secure
def hash(value1, value2):
    return (value1 + value2) % MODULO


class FRICommitment:

    def __init__(self, polynomial, num_points):
        if polynomial.p != MODULO:
            raise ValueError(f"Got polynomial over Z_{polynomial.p}, should be Z_{MODULO}")
        self.polynomial = polynomial
        values = list([polynomial(x) for x in range(num_points)])
        self.hashes = [values]
        while len(self.hashes[-1]) > 1:
            size = len(self.hashes[-1]) // 2
            parents = list([hash(
                    self.hashes[-1][2 * i],
                    self.hashes[-1][2 * i + 1]) for i in range(size)])
            self.hashes.append(parents)

    def __repr__(self):
        tree = ""
        for i in reversed(range(len(self.hashes))):
            tree += f"{self.hashes[i]}\n"
        return tree
    
    def prove_point_value(self, point):
        if point >= len(self.hashes[0]):
            raise ValueError(f"Considering a point outside the domain of commitment")
        merkle_proof = []
        for i in range(1, len(self.hashes)):
            parent = point >> i;
            triplet = (self.hashes[i][parent], self.hashes[i - 1][2 * parent], self.hashes[i - 1][2 * parent + 1])
            merkle_proof.append(triplet)
        return merkle_proof
    
def verify_point_value(point, value, merkle_proof):
    if merkle_proof[0][1 + point % 2] != value:
        return False
    for triplet in merkle_proof:
        if hash(triplet[1], triplet[2]) != triplet[0]:
            return False
    for i in range(1, len(merkle_proof)):
        if merkle_proof[i - 1][0] != merkle_proof[i][1] and merkle_proof[i - 1][0] != merkle_proof[i][2]:
            return False
    return True


if __name__ == "__main__":
    random.seed(0x31337)
    # Example commitment
    P = Polynomial([1, 4, 6, 4, 1], MODULO)
    NUM_POINTS = 2 << len(P.coefficients).bit_length()
    P_com = FRICommitment(P, NUM_POINTS)
    print(f"{P} is getting committed to")
    print(f"Merkle tree\n{P_com}")
    # Example FRI, follows Vitalik's notation
    Q, R = [], []
    for i, coeff in enumerate(P.coefficients):
        if i % 2 == 0:
            Q.append(coeff)
        else:
            R.append(coeff)
    Q = Polynomial(Q, MODULO)
    R = Polynomial(R, MODULO)
    Q_com = FRICommitment(Q, NUM_POINTS)
    R_com = FRICommitment(R, NUM_POINTS)
    print(f"P(x) = Q(x^2) + x * R(x^2)\nQ = {Q}\nR = {R}")
    print(f"Q merkle root {Q_com.hashes[-1][0]}, R merkle root {R_com.hashes[-1][0]}")
    r = random.randint(0, MODULO - 1)
    S = Q + R * r
    S_com = FRICommitment(S, NUM_POINTS)
    print(f"r = {r}")
    print(f"S = {S}")
    print(f"S merkle root {S_com.hashes[-1][0]}")
    print()

    point = random.randint(0, NUM_POINTS - 1)
    squared = (point * point) % MODULO
    print(f"Random coordinate point for verification {point}, squared {squared}")
    print(f"P({point}) = {P(point)}\nQ({squared}) = {Q(squared)}\nR({squared}) = {R(squared)}")
    print(f"Q(x^2) + x * R(x^2) = {(Q(squared) + point * R(squared)) % MODULO}")

    P_proof = P_com.prove_point_value(point)
    print(f"P proof {P_proof}")
    print("Verification: ", verify_point_value(point, P(point), P_proof))
    Q_proof = Q_com.prove_point_value(squared)
    print(f"Q proof {Q_proof}")
    print("Verification: ", verify_point_value(squared, Q(squared), Q_proof))
    R_proof = R_com.prove_point_value(squared)
    print(f"R proof {R_proof}")
    print("Verification: ", verify_point_value(squared, R(squared), R_proof))
    print()
