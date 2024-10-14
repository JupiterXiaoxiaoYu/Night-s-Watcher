// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;

import "../ERC20.sol";

contract TCB1_Rebasing is ERC20 {
    // --- Access Control ---
    using SafeMath for uint;
    address owner;
    uint256 public gonsPerFragment = 1e6;
    modifier auth() { require(msg.sender == owner, "unauthorised"); _; }
    event Rebase(uint256 supply);

    constructor(uint initTotalSupply) ERC20(initTotalSupply) {
        owner = msg.sender;
    }

    function balanceOf(address who)
        public
        view
        override
        returns (uint256)
    {
        return balances[who].div(gonsPerFragment);
    }

    function totalSupply()
        public
        view
        override
        returns (uint256)
    {
        return _totalSupply.div(gonsPerFragment);
    }

    function rebase(uint256 _newGonsPerFragment)
        external
        auth
        returns (uint256)
    {
        require(_newGonsPerFragment != 0, "new-gons-per-fragment-is-zero");
        gonsPerFragment = _newGonsPerFragment;
        emit Rebase(totalSupply());
        return totalSupply();
    }

    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        uint256 gonValue = wad.mul(gonsPerFragment);
        require(balanceOf(src) >= wad, "insufficient-balance");
        if (src != msg.sender && allowance[src][msg.sender] != type(uint).max) {
            require(allowance[src][msg.sender] >= wad, "insufficient-allowance");
            allowance[src][msg.sender] = allowance[src][msg.sender].sub(wad);
        }
        balances[src] = balances[src].sub(gonValue);
        balances[dst] = balances[dst].add(gonValue);
        emit Transfer(src, dst, wad);
        return true;
    }

    function _transfer(address src, address dst, uint wad) override internal returns (bool){
        uint256 gonValue = wad.mul(gonsPerFragment);
        balances[src] = balances[src].sub(gonValue);
        /// AssignmentMutation(`balances[dst].add(gonValue)` |==> `1`) of: `balances[dst] = balances[dst].add(gonValue);`
        balances[dst] = 1;
        emit Transfer(src, dst, wad);
        return true;

    }

    function getGonsPerFragment() public view returns(uint256){
        return gonsPerFragment;
    }

}