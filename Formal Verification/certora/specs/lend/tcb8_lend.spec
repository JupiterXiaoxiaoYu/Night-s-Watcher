using TCB8_Frozen as collateralToken;
using DummyWeth as lendingToken;
// using ERC20 as assetC;

methods
{
    function getCollectoralToken() external returns(address) envfree;
    function getLendingToken() external returns(address) envfree;
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function getPrice(address asset) external returns(uint256) envfree;
    function getTotalCollateral() external returns(uint256) envfree;
    function getTotalDeposit() external returns(uint256) envfree;
    function getTotalBorrow() external returns(uint256) envfree;
    function getUserDeposit(address user) external returns(uint256) envfree;
    function getUserBorrow(address user) external returns(uint256) envfree;
    function getUserCollateral(address user) external returns(uint256) envfree;
}

//P1
/**
* @title Prove that after operations the collectoral token balance records in the lending pool is same or less than the records in the Token contract
*/
rule PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 collateralPrice;
    uint256 lendingPrice;
    uint256 collateralBalanceReserve;
    uint256 collateralBalance;
    uint256 collateralBalanceReserveAfter;
    uint256 collateralBalanceAfter;

    collateralPrice = currentContract.getPrice(e, collateralToken);
    lendingPrice = currentContract.getPrice(e, lendingToken);
    require collateralPrice > 0 && lendingPrice > 0;

    collateralBalance = collateralToken.balanceOf(e, currentContract);
    collateralBalanceReserve = currentContract.totalCollateral;
    require collateralBalance > 0 && collateralBalance>=collateralBalanceReserve;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);

    collateralBalanceAfter = collateralToken.balanceOf(e, currentContract);
    collateralBalanceReserveAfter = currentContract.totalCollateral;

    assert collateralBalanceReserveAfter <= collateralBalanceAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2
/**
* @title Prove that after Liquidting the token gained by users is same or more than the pool has transferred
*/
rule PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred {
    env e;
    calldataarg args;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 collateralPrice;
    uint256 lendingPrice;

    uint256 collateralBalanceReserve;
    uint256 collateralBalance;

    uint256 collateralBalanceReserveAfter;
    uint256 collateralBalanceAfter;

    uint256 userCollateralBalance;
    uint256 userCollateralBalanceAfter;

    collateralPrice = currentContract.getPrice(e, collateralToken);
    lendingPrice = currentContract.getPrice(e, lendingToken);
    require collateralPrice > 0 && lendingPrice > 0;

    collateralBalance = collateralToken.balanceOf(e, currentContract);
    collateralBalanceReserve = currentContract.getTotalCollateral(e);

    require collateralBalance > 0 && collateralBalance>=collateralBalanceReserve;
    userCollateralBalance = collateralToken.balanceOf(e, e.msg.sender);

    require e.msg.sender != currentContract;
    currentContract.liquidate(e,args);

    collateralBalanceAfter = collateralToken.balanceOf(e, currentContract);
    userCollateralBalanceAfter = collateralToken.balanceOf(e, e.msg.sender);

    assert collateralBalance - collateralBalanceAfter <= userCollateralBalanceAfter - userCollateralBalance,
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

// //P3
// /**
// * @title Prove that after withrawlCollectoral the collectoral token gained by users is same or more than the pool has transferred
// * @dev The token gained by users removing liquidity is same or more than the pool has transferred
// */

rule PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred {
    env e;
    calldataarg args;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 collateralPrice;
    uint256 lendingPrice;

    uint256 collateralBalanceReserve;
    uint256 collateralBalance;

    uint256 collateralBalanceAfter;

    uint256 userCollateralBalance;
    uint256 userCollateralBalanceAfter;

    collateralPrice = currentContract.getPrice(e, collateralToken);
    lendingPrice = currentContract.getPrice(e, lendingToken);
    require collateralPrice > 0 && lendingPrice > 0;
    
    collateralBalanceReserve = currentContract.getTotalCollateral(e);
    collateralBalance = collateralToken.balanceOf(e, currentContract);

    require collateralBalance > 0 && collateralBalance>=collateralBalanceReserve;
    userCollateralBalance = collateralToken.balanceOf(e, e.msg.sender);

    require e.msg.sender != currentContract;
    currentContract.withdrawCollateral(e,args);

    collateralBalanceAfter = collateralToken.balanceOf(e, currentContract);
    userCollateralBalanceAfter = collateralToken.balanceOf(e, e.msg.sender);

    assert collateralBalance - collateralBalanceAfter <= userCollateralBalanceAfter - userCollateralBalance,
    "The liquidity / token gained by users is same or more than the pool has transferred";
}


//P4
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 collateralPrice;
    uint256 lendingPrice;
    uint256 collateralBalance;
    uint256 userCollateralBalance;
    mathint totalSupplyCollateral;

    collateralPrice = currentContract.getPrice(e, collateralToken);
    lendingPrice = currentContract.getPrice(e, lendingToken);
    require collateralPrice > 0 && lendingPrice > 0;

    collateralBalance = collateralToken.balanceOf(e, currentContract);

    userCollateralBalance = collateralToken.balanceOf(e, e1.msg.sender);
    totalSupplyCollateral = collateralToken.totalSupply(e);

    require collateralBalance > 0 && userCollateralBalance > 0 && collateralBalance+userCollateralBalance <= totalSupplyCollateral;
    require e.msg.sender != e1.msg.sender && e.msg.sender == currentContract;

    collateralToken.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, collateralBalance);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 userBalanceOfCollateral;
    uint256 userBalanceOfCollateralAfter;
    uint256 amountCollateralIn;
    uint256 collateralBalance;
    mathint totalCollateralSupply;
    uint256 collateralBalanceReserve;

    collateralBalance = collateralToken.balanceOf(e, currentContract);
    collateralBalanceReserve = currentContract.getTotalCollateral(e);
    totalCollateralSupply = collateralToken.totalSupply(e);
    userBalanceOfCollateral = currentContract.getUserCollateral(e, e.msg.sender);
    
    require amountCollateralIn > 0;
    require collateralBalanceReserve <= collateralBalance;
    require totalCollateralSupply >= collateralBalance + amountCollateralIn;
    require e.msg.sender != currentContract;
    require userBalanceOfCollateral == 0;

    currentContract.depositCollateral(e, amountCollateralIn);
    
    userBalanceOfCollateralAfter = currentContract.getUserCollateral(e, e.msg.sender);

    assert userBalanceOfCollateralAfter > 0;
}

//P6
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getCollectoralToken() == collateralToken && getLendingToken() == lendingToken;
    uint256 userBalanceOfCollateral;
    uint256 userBalanceOfCollateralAfter;
    uint256 userBalanceOfCollateralDeposited;
    uint256 claimableFee;
    uint256 claimableFeeAfter;
    uint256 balanceOfCollateral;

    require e.msg.sender != currentContract;

    balanceOfCollateral = collateralToken.balanceOf(e, currentContract);
    userBalanceOfCollateral = collateralToken.balanceOf(e, e.msg.sender);
    claimableFee = currentContract.getClaimableFee(e, e.msg.sender);

    require balanceOfCollateral > claimableFee;

    userBalanceOfCollateralDeposited = currentContract.getUserDeposit(e, e.msg.sender);

    require userBalanceOfCollateral == 0 && userBalanceOfCollateralDeposited > 0 && claimableFee > 0;

    currentContract.claimFee(e);

    userBalanceOfCollateralAfter = collateralToken.balanceOf(e, e.msg.sender);

    claimableFeeAfter = currentContract.getClaimableFee(e, e.msg.sender);

    assert userBalanceOfCollateralAfter > 0 && claimableFeeAfter == 0;
}