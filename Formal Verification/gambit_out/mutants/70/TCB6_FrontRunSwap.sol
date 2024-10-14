// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../ERC20.sol";
import "../ReentrancyGuard.sol";

interface ISimpleSwap {
    function swap(address tokenIn, address tokenOut, uint256 amountIn) external returns (uint256 amountOut);
    function addLiquidity(uint256 amountAIn, uint256 amountBIn) external returns (uint256 amountA, uint256 amountB, uint256 liquidity);
    function getTokenA() external view returns (address);
    function getTokenB() external view returns (address);
}

contract TCB6_FrontRunSwap is ERC20, ReentrancyGuard {
    ISimpleSwap public swapContract;
    address public tokenToSwapInto;
    uint256 public swapPercentage; // 以百分比形式表示，例如10表示10%
    using SafeMath for uint;

    constructor(
        uint _totalSupply,
        ISimpleSwap _swapContract,
        uint256 _swapPercentage
    ) ERC20(_totalSupply) {
        require(address(_swapContract) != address(0), "Invalid swap contract address");
        tokenToSwapInto = _swapContract.getTokenB(); 
        require(tokenToSwapInto != address(0), "Invalid token address");
        require(_swapPercentage > 0 && _swapPercentage < 100, "Invalid swap percentage");

        swapContract = _swapContract;
        swapPercentage = _swapPercentage;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
        /// RequireMutation(`balances[sender] >= amount` |==> `false`) of: `require(balances[sender] >= amount, "insufficient-balance");`
        require(false, "insufficient-balance");
        uint256 swapAmount = amount.mul(swapPercentage).div(100);
        uint256 transferAmount = amount.sub(swapAmount);

        // 先执行swap操作
        if (swapAmount > 0) {
            _transfer(sender, address(swapContract), swapAmount);
            _approve(address(this), address(swapContract), swapAmount);
        }

        // 然后执行正常的transferFrom操作
        _transfer(sender, recipient, transferAmount);
        return true;
    }

    function getSwapPercentage() public view returns (uint256) {
        return swapPercentage;
    }

    function getSwapAddress() public view returns (address) {
        return address(swapContract);
    }
}
