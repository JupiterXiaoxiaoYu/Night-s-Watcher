// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity ^0.8.8;

import "../ERC20.sol";

contract TCB3_Inflation_Airdrop is ERC20 {
    uint256 _airdropAmount;
    uint256 _cutoff = _airdropAmount * 10000;
    uint256 _outAmount = 0;
    using SafeMath for uint;

    mapping(address => bool) initialized;

    constructor(
        uint256 airdropAmount
    ) ERC20(airdropAmount * 19000000) {
        /// RequireMutation(`airdropAmount > 0` |==> `false`) of: `require(airdropAmount > 0, "airdrop-amount-is-zero");`
        require(false, "airdrop-amount-is-zero");
        require(airdropAmount.mul(19000000).add(_cutoff) < type(uint256).max, "airdrop-amount-too-high");
        initialized[msg.sender] = true;
        _airdropAmount = airdropAmount;
    }

    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        require(balances[src] >= wad, "insufficient-balance");
        if (src != msg.sender && allowance[src][msg.sender] != type(uint).max) {
            require(allowance[src][msg.sender] >= wad, "insufficient-allowance");
            allowance[src][msg.sender] = allowance[src][msg.sender].sub(wad);
        }
        balances[src] = balances[src].sub(wad);
        balances[dst] = balances[dst].add(wad);
        initialize(src);
        initialize(dst);
        emit Transfer(src, dst, wad);
        return true;
    }

    // internal privats
    function initialize(address _address) internal returns (bool success) {
        if (_outAmount < _cutoff && !initialized[_address]) {
            initialized[_address] = true;
            balances[_address].add(_airdropAmount);
            _outAmount = _outAmount.add(_airdropAmount);
            _totalSupply = _totalSupply.add(_airdropAmount);
            return true;
        }
        return false;
    }

    function getAirDropAmount() public view returns(uint256 amount){
        return _airdropAmount;
    }

    function getCutoff() public view returns(uint256 amount){
        return _cutoff;
    }

    function isInitialized(address _address) public view returns(bool success){
        return initialized[_address];
    }

    function getOutAmount() public view returns(uint256 amount){
        return _outAmount;
    }
    
}