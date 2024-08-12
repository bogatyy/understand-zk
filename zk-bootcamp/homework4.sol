// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BN128CurveOperations {
    // Address of the precompiled contract for BN128 addition
    address constant BN128_ADD = address(6);

    // Address of the precompiled contract for BN128 scalar multiplication
    address constant BN128_MUL = address(7);

    /**
     * @dev Adds two BN128 curve points using the precompiled contract.
     */
    function bn128Add(uint256 x1, uint256 y1, uint256 x2, uint256 y2) public view returns (uint256, uint256) {
        bytes memory input = abi.encodePacked(x1, y1, x2, y2);
        (bool success, bytes memory result) = BN128_ADD.staticcall(input);
        require(success, "BN128 addition failed");
        return abi.decode(result, (uint256, uint256));
    }

    /**
     * @dev Multiplies a BN128 curve point by a scalar using the precompiled contract.
     */
    function bn128Mul(uint256 x, uint256 y, uint256 scalar) public view returns (uint256, uint256) {
        bytes memory input = abi.encodePacked(x, y, scalar);
        (bool success, bytes memory result) = BN128_MUL.staticcall(input);
        require(success, "BN128 multiplication failed");
        return abi.decode(result, (uint256, uint256));
    }

    struct ECPoint {
        uint256 x;
        uint256 y;
    }

    /**
     * @dev Verifies if two elliptic curve points add up to num/den * G1
     */
    function rationalAdd(
        ECPoint calldata A,
        ECPoint calldata B,
        uint256 num,
        uint256 den
    ) public view returns (bool) {
        // A + B == num/den * G1
        // (A + B) * den == G1 * num
        (uint256 abx, uint256 aby) = bn128Add(A.x, A.y, B.x, B.y);
        (uint256 x1, uint256 y1) = bn128Mul(abx, aby, den);
        (uint256 x2, uint256 y2) = bn128Mul(1, 2, num);
        return (x1 == x2 && y1 == y2);
    }

    /**
     * @dev Verifies that M * s == o
     */
    function matmul(
        uint256 n, 
        uint256[] calldata matrix, // n x n elements
        ECPoint[] calldata s, // n elements
        uint256[] calldata o // n elements
    ) public view returns (bool verified) {
        // Revert if dimensions don't make sense or the matrices are empty
        require(n > 0, "Must have more than zero elements");
        require(matrix.length == n * n, "Matrix must have n x n elements");
        require(s.length == n, "Vector s must have n elements");
        require(o.length == n, "Vector o must have n elements");

        // Return true if Ms == o element-wise
        for (uint256 i = 0; i < n; i++) {
            // Ethereum precompiles represent the identity point as (0, 0)
            (uint256 sumX, uint256 sumY) = (0, 0);
            for (uint256 j = 0; j < n; j++) {
                // Multiply matrix element by the corresponding vector element s[j]
                (uint256 curX, uint256 curY) = bn128Mul(s[j].x, s[j].y, matrix[i * n + j]);
                (sumX, sumY) = bn128Add(sumX, sumY, curX, curY);
            }
            // Multiply the output o[i] by the generator G1
            (uint256 oG1x, uint256 oG1y) = bn128Mul(1, 2, o[i]);
            // Check if the resulting point from Ms equals oG1
            if (sumX != oG1x || sumY != oG1y) {
                return false;
            }
        }
        return true;
    }
}
