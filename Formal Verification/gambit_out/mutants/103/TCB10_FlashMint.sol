// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../ERC20.sol";
import "../ReentrancyGuard.sol";

contract TCB10_FlashMint is ERC20, ReentrancyGuard {
    uint256 private constant MAX_SUPPLY = type(uint256).max;
    uint256 public flashMintFee;
    uint256 public feePrecision = 1000;

    // FlashMint 事件
    event FlashMint(address indexed to, uint256 amount);

    constructor(uint _totalSupply, uint256 _fee) ERC20(_totalSupply)  {
        require(_fee < 100, "FlashMint: fee too high");
        flashMintFee = _fee;
    }

    function calcPremium(uint256 amount) public view returns (uint256){
        return ((amount*flashMintFee)/feePrecision);
    }

    // FlashMint 函数
    function flashMint(address receiverAddress, uint256 amount) public nonReentrant {
        require(totalSupply() + amount <= MAX_SUPPLY, "FlashMint: cap exceeded");
        uint256 totalPremium = calcPremium(amount);

        uint256 amountPlusPremium = amount + totalPremium;
        _mint(receiverAddress, amount);

        /// RequireMutation(`IFlashMintReceiver(receiverAddress).executeOperation(amount,totalPremium,msg.sender)` |==> `true`) of: `require(IFlashMintReceiver(receiverAddress).executeOperation(amount,totalPremium,msg.sender));`
        require(true);

        _burn(receiverAddress, amountPlusPremium);

        emit FlashMint(receiverAddress, amount);
    }
}

interface IFlashMintReceiver {
    function executeOperation(uint256 amount,uint256 premium,address initiator) external returns (bool);
}
