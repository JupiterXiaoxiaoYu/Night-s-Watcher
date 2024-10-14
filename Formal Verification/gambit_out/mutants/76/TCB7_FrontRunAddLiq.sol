// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

import "../ERC20.sol";
import "../ReentrancyGuard.sol";

interface ISimpleSwap {
    function swap(address tokenIn, address tokenOut, uint256 amountIn) external returns (uint256 amountOut);
    function addLiquidity(uint256 amountAIn, uint256 amountBIn) external returns (uint256 amountA, uint256 amountB, uint256 liquidity);
    function getTokenA() external view returns (address);
    function getTokenB() external view returns (address);
}

contract TCB7_FrontRunAddLiq is ERC20, ReentrancyGuard {
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
        tokenToSwapInto = _swapContract.getTokenB(); // 假设当前合约代币为TokenA，要交换成TokenB
        require(tokenToSwapInto != address(0), "Invalid token address");
        /// RequireMutation(`_swapPercentage > 0 && _swapPercentage < 100` |==> `false`) of: `require(_swapPercentage > 0 && _swapPercentage < 100, "Invalid swap percentage");`
        require(false, "Invalid swap percentage");

        swapContract = _swapContract;
        swapPercentage = _swapPercentage;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
        uint256 swapAmount = (amount.mul(swapPercentage)).div(100);
        uint256 transferAmount = amount - swapAmount;

        // 先执行swap操作
        if (swapAmount > 0) {
            uint256 half = swapAmount.div(2);
            _transfer(sender, address(swapContract), half);
            _approve(address(this), address(swapContract), swapAmount);
            // uint256 swappedAmount = swapContract.swap(address(this), tokenToSwapInto, half);
            // ERC20(tokenToSwapInto).approve(address(swapContract), swappedAmount);
            // swapContract.addLiquidity(swapAmount, swappedAmount);
        }

        // 然后执行正常的transferFrom操作
        _transfer(sender, recipient, transferAmount);
        return true;
    }

    function getSwapAddress() public view returns (address) {
        return address(swapContract);
    }

    function getSwapPercentage() public view returns (uint256) {
        return swapPercentage;
    }


}
