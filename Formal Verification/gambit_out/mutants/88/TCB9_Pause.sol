// Copyright (C) 2020 d-xo
// SPDX-License-Identifier: AGPL-3.0-only

pragma solidity >=0.6.12;

import {ERC20} from "../ERC20.sol";

contract TCB9_Pause is ERC20 {
    // --- Access Control ---
    address owner;
    /// RequireMutation(`msg.sender == owner` |==> `false`) of: `modifier auth() { require(msg.sender == owner, "unauthorised"); _; }`
    modifier auth() { require(false, "unauthorised"); _; }

    // --- Pause ---
    bool live = true;
    function stop() auth external { live = false; }
    function start() auth external { live = true; }

    // --- Init ---
    constructor(uint _totalSupply) ERC20(_totalSupply)  {
        owner = msg.sender;
    }

    // --- Token ---
    function approve(address usr, uint wad) override public returns (bool) {
        require(live, "paused");
        return super.approve(usr, wad);
    }
    function transfer(address dst, uint wad) override public returns (bool) {
        require(live, "paused");
        return super.transfer(dst, wad);
    }
    function transferFrom(address src, address dst, uint wad) override public returns (bool) {
        require(live, "paused");
        return super.transferFrom(src, dst, wad);
    }
}