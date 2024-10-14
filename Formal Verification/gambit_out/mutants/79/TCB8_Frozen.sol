// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;

import "../ERC20.sol";

contract TCB8_Frozen is ERC20 {
    // --- Access Control ---
    address owner;
    /// RequireMutation(`msg.sender == owner` |==> `true`) of: `modifier auth() { require(msg.sender == owner, "unauthorised"); _; }`
    modifier auth() { require(true, "unauthorised"); _; }

    // --- BlockList ---
    mapping(address => bool) blocked;
    function blockUser(address usr) auth public { blocked[usr] = true; }
    function allow(address usr) auth public { blocked[usr] = false; }

    // --- Init ---
    constructor(uint _totalSupply) ERC20(_totalSupply) {
        owner = msg.sender;
    }

    // --- Token ---
    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        require(!blocked[src], "blocked");
        require(!blocked[dst], "blocked");
        return super.transferFrom(src, dst, wad);
    }
}