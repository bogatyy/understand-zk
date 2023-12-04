def extended_euclidean(a, b):
    """
    Extended Euclidean Algorithm to find the multiplicative inverse of a in Z_p.
    """
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = extended_euclidean(b, a % b)
        return gcd, y, x - (a // b) * y

def mod_inv(a, p):
    """
    Find the multiplicative inverse of a in Z_p using the Extended Euclidean Algorithm.
    """
    gcd, x, _ = extended_euclidean(a, p)
    if gcd != 1:
        raise ValueError(f"No inverse exists for {a} in Z_{p}")
    else:
        return x % p


class Polynomial:

    def __init__(self, coefficients, p):
        """
        Initializes a new Polynomial object.
        :param coefficients: A list of coefficients, where the i-th element is the coefficient for x^i.
        :param p: The prime for the field Z_p.
        """
        self.coefficients = [c % p for c in coefficients]  # Reduce all coefficients modulo p
        self.p = p

    def __call__(self, x):
        """
        Evaluate the polynomial at a given point x.
        """
        result = 0
        multiple = 1
        for coeff in self.coefficients:
            result = (result + coeff * multiple) % self.p
            multiple = (multiple * x) % self.p
        return result

    def __add__(self, other):
        """
        Adds this polynomial to another polynomial.
        """
        if self.p != other.p:
            raise ValueError("Cannot add polynomials in different fields")

        # Get the length of the longer polynomial
        length = max(len(self.coefficients), len(other.coefficients))
        result = [0] * length

        for i in range(length):
            c1 = self.coefficients[i] if i < len(self.coefficients) else 0
            c2 = other.coefficients[i] if i < len(other.coefficients) else 0
            result[i] = (c1 + c2) % self.p

        return Polynomial(result, self.p)

    def __mul__(self, other):
        """
        Multiplies this polynomial with another polynomial.
        """
        if self.p != other.p:
            raise ValueError("Cannot multiply polynomials in different fields")

        # Prepare the result array
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)

        # Perform multiplication
        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                result[i + j] = (result[i + j] + self.coefficients[i] * other.coefficients[j]) % self.p

        return Polynomial(result, self.p)

    def __truediv__(self, other):
        """
        Divides this polynomial by another polynomial, returning the quotient and remainder.
        Assumes the leading coefficient of the divisor is invertible in Z_p.
        """
        if self.p != other.p:
            raise ValueError("Cannot divide polynomials in different fields")

        # Copy the dividend (self) and divisor (other)
        dividend = self.coefficients[:]
        divisor = other.coefficients[:]
        quotient = [0] * (len(dividend) - len(divisor) + 1)

        # Leading coefficient of the divisor and its inverse in Z_p
        leading_coeff = divisor[0]
        inv_leading_coeff = mod_inv(leading_coeff, self.p)

        for i in range(len(dividend) - len(divisor) + 1):
            # Scale factor to multiply the divisor by at each step
            scale = dividend[i] * inv_leading_coeff % self.p
            quotient[i] = scale

            for j in range(len(divisor)):
                # Subtract the scaled divisor from the dividend
                dividend[i + j] = (dividend[i + j] - scale * divisor[j]) % self.p

        # The remainder is what's left in the dividend after division
        remainder = dividend[len(divisor) - 1:]

        return Polynomial(quotient, self.p), Polynomial(remainder, self.p)

    def __repr__(self):
        return f"Polynomial({self.coefficients}, {self.p})"


if __name__ == "__main__":
    # Example usage
    p1 = Polynomial([4, 4, 4], 5)  # Represents 3x^2 + 2x + 1 in Z_5
    p2 = Polynomial([3, 3], 5)     # Represents x + 4 in Z_5

    # Polynomial addition and multiplication
    sum_poly = p1 + p2
    product_poly = p1 * p2

    print(f"{p1} + {p2} = {sum_poly}")
    print(f"{p1} * {p2} = {product_poly}")

    # Example usage
    p1 = Polynomial([1, 0, 5, 4], 7)  # Represents x^3 + 5x + 4 in Z_7
    p2 = Polynomial([1, 2], 7)        # Represents x + 2 in Z_7

    # Polynomial division
    quotient, remainder = p1 / p2

    print(f"quotient {quotient} and remainder {remainder}")
    print(p1)
    print(quotient * p2 + remainder)
