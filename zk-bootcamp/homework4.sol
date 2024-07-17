// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BN128CurveOperations {

    // Address of the precompiled contract for BN128 addition
    address constant BN128_ADD = 0x06;
    
    // Address of the precompiled contract for BN128 scalar multiplication
    address constant BN128_MUL = 0x07;

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
    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool) {
        // A + B == num/den * G1
        // (A + B) * den == G1 * num
        (uint256 abx, uint256 aby) = bn128Add(A.x, A.y, B.x, B.y);
        (uint256 x1, uint256 y1) = bn128Mul(abx, aby, den);
        (uint256 x2, uint256 y2) = bn128Mul(1, 2, num);
        return (x1 == x2 && y1 == y2);
    }
}
