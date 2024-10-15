// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;

import "../ERC20.sol";

contract TCB8_Frozen is ERC20 {
    // --- Access Control ---
    address owner;
    modifier auth() { require(msg.sender == owner, "unauthorised"); _; }

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
        /// RequireMutation(`!blocked[src]` |==> `false`) of: `require(!blocked[src], "blocked");`
        require(false, "blocked");
        require(!blocked[dst], "blocked");
        return super.transferFrom(src, dst, wad);
    }
}