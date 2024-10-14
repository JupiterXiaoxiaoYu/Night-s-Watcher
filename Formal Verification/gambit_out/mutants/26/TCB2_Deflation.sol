// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity >=0.6.12;

import "../ERC20.sol";

contract TCB2_Deflation is ERC20 {
    using SafeMath for uint;
    uint immutable fee = 10;
    uint immutable feeDenominator = 1000;

    // --- Init ---
    constructor(uint _totalSupply, uint _fee) ERC20(_totalSupply) {
    }

    // --- Token ---
    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        require(balances[src] >= wad, "insufficient-balance");
        require(wad > 0, "zero-value-transfer");
        if (src != msg.sender && allowance[src][msg.sender] != type(uint).max) {
            require(allowance[src][msg.sender] >= wad, "insufficient-allowance");
            allowance[src][msg.sender] = allowance[src][msg.sender].sub(wad);
        }
        uint feeAmount = wad.mul(fee).div(feeDenominator);
        uint wadAfterFee = wad.sub(feeAmount);
        /// AssignmentMutation(`balances[src].sub(wad)` |==> `0`) of: `balances[src] = balances[src].sub(wad);`
        balances[src] = 0;
        balances[dst] = balances[dst].add(wadAfterFee);
        // Instead of transferring fee to address(0), we subtract it from the total supply
        _totalSupply = _totalSupply.sub(feeAmount);

        emit Transfer(src, dst, wadAfterFee);
        // This event logs the fee burn
        emit Transfer(src, address(0), feeAmount);
        return true;
    }
}
