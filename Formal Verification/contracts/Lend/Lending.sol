// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity 0.8.19;

import "../IERC20.sol";
import "../ReentrancyGuard.sol";

interface IPriceOracle {
    function getPrice(address asset) external view returns (uint256);
}

contract Lending is ReentrancyGuard{
    IERC20 public lendingToken; // 用于借贷的代币
    IERC20 public collateralToken; // 用于抵押的代币
    IPriceOracle public priceOracle;

    uint256 public constant feeRate = 3; 
    uint256 public constant feeDenominator = 1000;

    uint256 public accumulatedFee;
    mapping(address => uint256) private claimedFee;

    mapping(address => uint256) public deposits; // 记录借贷代币的存款
    mapping(address => uint256) public collaterals; // 记录抵押代币的抵押量
    mapping(address => uint256) public borrows; // 记录借贷代币的借款量

    uint256 public constant MARGIN_RATE = 150e16; // 保证金率150%
    uint256 public totalBorrow; // 总借款量
    uint256 public totalDeposit; // 总存款量
    uint256 public totalCollateral; // 总抵押量

    event Deposit(address indexed depositor, uint256 amount);
    event Withdraw(address indexed depositor, uint256 amount);
    event Borrow(address indexed borrower, uint256 amount);
    event Repay(address indexed borrower, uint256 amount);
    event Liquidate(address indexed borrower, address indexed liquidator, uint256 liquidatedCollateralAmount);
    event CollateralDeposited(address indexed depositor, uint256 amount);
    event CollateralWithdrawn(address indexed depositor, uint256 amount);

    constructor(IERC20 _lendingToken, IERC20 _collateralToken, IPriceOracle _priceOracle) {
        lendingToken = _lendingToken;
        collateralToken = _collateralToken;
        priceOracle = _priceOracle;
    }

    function getUserDeposit(address user) public view returns (uint256) {
        return deposits[user];
    }

    function getUserCollateral(address user) public view returns (uint256) {
        return collaterals[user];
    }

    function getUserBorrow(address user) public view returns (uint256) {
        return borrows[user];
    }
    
    function getCollectoralToken() public view returns (address) {
        return address(collateralToken);
    }

    function getLendingToken() public view returns (address) {
        return address(lendingToken);
    }

    function getTotalCollateral() public view returns (uint256) {
        return totalCollateral;
    }

    function getTotalDeposit() public view returns (uint256) {
        return totalDeposit;
    }

    function getTotalBorrow() public view returns (uint256) {
        return totalBorrow;
    }

    function getPrice(address asset) public view returns (uint256) {
        return priceOracle.getPrice(asset);
    }

    function depositCollateral(uint256 amount) public nonReentrant{
        require(amount > 0, "Amount must be greater than 0");
        collaterals[msg.sender] += amount;
        totalCollateral += amount;
        collateralToken.transferFrom(msg.sender, address(this), amount);
        emit CollateralDeposited(msg.sender, amount);
    }

    function withdrawCollateral(uint256 amount) public nonReentrant {
        require(amount <= collaterals[msg.sender], "Insufficient collateral balance");
        collaterals[msg.sender] -= amount;
        totalCollateral -= amount;
        collateralToken.transferFrom(msg.sender,address(this), amount);
        emit CollateralWithdrawn(msg.sender, amount);
    }

    function borrow(uint256 amount) public {
        uint256 collateralPrice = priceOracle.getPrice(address(collateralToken));
        uint256 lendingPrice = priceOracle.getPrice(address(lendingToken));

        // 使用抵押代币的市场价值来计算最大可借金额
        uint256 maxBorrowValue = collaterals[msg.sender] * collateralPrice / 1e18;
        uint256 currentBorrowValue = borrows[msg.sender] * lendingPrice / 1e18;
        require(currentBorrowValue + (amount * lendingPrice / 1e18) <= maxBorrowValue * MARGIN_RATE / 1e18, "Borrow amount exceeds margin");

        borrows[msg.sender] += amount;
        lendingToken.transfer(msg.sender, amount);
        totalBorrow += amount;
        emit Borrow(msg.sender, amount);
    }

    function repay(uint256 amount) public nonReentrant{
        require(borrows[msg.sender] >= amount, "Repay amount exceeds borrow balance");
        borrows[msg.sender] -= amount;
        totalBorrow -= amount;
        lendingToken.transferFrom(msg.sender, address(this), amount);
        uint256 fee = amount * feeRate / feeDenominator;
        collateralToken.transferFrom(msg.sender, address(this), fee);
        emit Repay(msg.sender, amount);
    }

    function liquidate(address borrower) public nonReentrant{
        uint256 collateralPrice = priceOracle.getPrice(address(collateralToken));
        uint256 lendingPrice = priceOracle.getPrice(address(lendingToken));

        uint256 borrowValue = borrows[borrower] * lendingPrice / 1e18;
        uint256 collateralValue = collaterals[borrower] * collateralPrice / 1e18;

        // 检查是否需要清算
        require(collateralValue < borrowValue * MARGIN_RATE / 1e18, "Borrow is safe");

        // 执行清算逻辑
        uint256 liquidationAmount = borrows[borrower];
        totalBorrow -= borrows[borrower];
        borrows[borrower] = 0;
        uint256 liquidatedCollateralAmount = liquidationAmount * lendingPrice / collateralPrice;
        collaterals[borrower] -= liquidatedCollateralAmount;

        collateralToken.transferFrom(address(this), msg.sender, liquidatedCollateralAmount);
        totalCollateral -= liquidatedCollateralAmount;
        emit Liquidate(borrower, msg.sender, liquidatedCollateralAmount);
    }

    function claimFee() public nonReentrant {
        require(collaterals[msg.sender] > 0, "No Colleral to claim fee");
        
        uint256 userTotalShare = (collaterals[msg.sender] * accumulatedFee) / totalCollateral;
        
        uint256 claimableFee = userTotalShare - claimedFee[msg.sender];

        require(claimableFee > 0, "No fees to claim");
        
        claimedFee[msg.sender] = userTotalShare;
        collateralToken.transferFrom(address(this),msg.sender, claimableFee);
        
    }

    function getClaimableFee(address user) public view returns (uint256) {
        uint256 userTotalShare = (collaterals[user] * accumulatedFee) / totalCollateral;
        uint256 claimableFee = userTotalShare - claimedFee[user];
        return claimableFee;
    }

}
