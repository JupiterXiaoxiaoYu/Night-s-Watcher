// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;

import "../ERC20.sol";

contract TCB4_Fee is ERC20 {

    uint immutable fee;
    using SafeMath for uint;
    // --- Init ---
    constructor(uint _totalSupply, uint _fee) ERC20(_totalSupply) {
        fee = _fee;
    }

    // --- Token ---
    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        require(balances[src] >= wad, "insufficient-balance");
        if (src != msg.sender && allowance[src][msg.sender] != type(uint).max) {
            require(allowance[src][msg.sender] >= wad, "insufficient-allowance");
            allowance[src][msg.sender] = allowance[src][msg.sender].sub(wad);
        }

        balances[src] = balances[src].sub(wad);
        /// AssignmentMutation(`balances[dst].add(wad.sub(fee))` |==> `0`) of: `balances[dst] = balances[dst].add(wad.sub(fee));`
        balances[dst] = 0;
        balances[address(0)] = balances[address(0)].add(fee);

        emit Transfer(src, dst, wad.sub(fee));
        emit Transfer(src, address(0), fee);

        return true;
    }
}