// Copyright (C) 2017, 2018, 2019, 2020 dbrock, rain, mrchico, d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;
import {SafeMath} from "./SafeMath.sol";

contract ERC20  {
    // --- ERC20 Data ---
    using SafeMath for uint;
    string  public constant name = "Token";
    string  public constant symbol = "TKN";
    uint8   public decimals = 18;
    uint256 internal _totalSupply;

    mapping (address => uint)                      internal balances;
    mapping (address => mapping (address => uint)) internal allowance;

    event Approval(address indexed src, address indexed guy, uint wad);
    event Transfer(address indexed src, address indexed dst, uint wad);

    // --- Init ---
    constructor(uint initTotalSupply) {
        _totalSupply = initTotalSupply;
        balances[msg.sender] = _totalSupply;
        emit Transfer(address(0), msg.sender, _totalSupply);
    }


    // --- Token ---
    function transfer(address dst, uint wad) virtual public returns (bool) {
        return _transfer(msg.sender, dst, wad);
    }

    function totalSupply() virtual public view returns (uint) {
        return _totalSupply;
    }

    function balanceOf(address guy) virtual public view returns (uint) {
        return balances[guy];
    }

    function transferFrom(address src, address dst, uint wad) virtual public returns (bool) {
        require(balances[src] >= wad, "insufficient-balance");
        if (src != msg.sender && allowance[src][msg.sender] != type(uint).max) {
            require(allowance[src][msg.sender] >= wad, "insufficient-allowance");
            allowance[src][msg.sender] = allowance[src][msg.sender].sub(wad);
        }
        balances[src] = balances[src].sub(wad);
        balances[dst] = balances[dst].add(wad);
        emit Transfer(src, dst, wad);
        return true;
    }

    function approve(address usr, uint wad) virtual public returns (bool) {
        return _approve(msg.sender, usr, wad);
    }

    function _approve(address src, address usr, uint wad) virtual internal returns (bool){
        allowance[src][usr] = wad;
        emit Approval(src, usr, wad);
        return true;
    }

    function _mint(address usr, uint wad) virtual internal {
        balances[usr] = balances[usr].add(wad);
        _totalSupply = _totalSupply.add(wad);
        emit Transfer(address(0), usr, wad);
    }

    function _burn(address usr, uint wad) virtual internal {
        balances[usr] = balances[usr].sub(wad);
        _totalSupply = _totalSupply.sub(wad);
        emit Transfer(usr, address(0), wad);
    }

    function _transfer(address src, address dst, uint wad) virtual internal returns (bool){
        /// AssignmentMutation(`balances[src].sub(wad)` |==> `1`) of: `balances[src] = balances[src].sub(wad);`
        balances[src] = 1;
        balances[dst] = balances[dst].add(wad);
        emit Transfer(src, dst, wad);
        return true;
    }
}