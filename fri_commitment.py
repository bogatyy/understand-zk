from polynomial import Polynomial


def hash(value1, value2, p):
    return (value1 + value2) % p


class FRICommitment:

    def __init__(self, polynomial):
        p = polynomial.p
        self.polynomial = polynomial
        degree = len(polynomial.coefficients) + 1
        num_points = 2 << (degree - 1).bit_length()
        points = list(range(num_points))
        values = list([polynomial(x) for x in points])
        self.hashes = [values]
        while len(self.hashes[-1]) > 1:
            size = len(self.hashes[-1]) // 2
            parents = list([hash(
                    self.hashes[-1][2 * i],
                    self.hashes[-1][2 * i + 1], p) for i in range(size)])
            self.hashes.append(parents)

    def __repr__(self):
        tree = ""
        for i in reversed(range(len(self.hashes))):
            tree += f"{self.hashes[i]}\n"
        return tree

if __name__ == "__main__":
    # Example usage
    p = Polynomial([1, 2, 1], 5)
    com = FRICommitment(p)
    print(f"{p} is getting committed to")
    print(f"Commitment\n{com}")
