using DummyWeth as assetB;
using TCB3_Inflation_Airdrop as TCB3;
// using ERC20 as assetC;

methods
{
    function swap(address, address, uint256)         internal returns(uint256);
    function getTokenA() external returns(address) envfree;
    function getTokenB() external returns(address) envfree;
    function getReserves() external returns(uint256, uint256) envfree;
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.getAirDropAmount() external => DISPATCHER(true);
    function _.getOutAmount() external => DISPATCHER(true);
    function _.isInitialized(address) external => DISPATCHER(true);
}

//P1_TCB3
/**
* @title Prove that after operations the liquidity records in the pool is same or less than the records in the Token contract
* @dev The liquidity records in the pool is same or less than the records in the Token contract
*/
rule TCB3_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB3 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 airdropAmount;
    uint256 outAmount;
    mathint totalSupplyA;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB3.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);
    airdropAmount = TCB3.getAirDropAmount(e);
    outAmount = TCB3.getOutAmount(e);
    totalSupplyA = TCB3.totalSupply(e);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;
    require balanceOfA + airdropAmount + airdropAmount + outAmount < totalSupplyA;
    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB3.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB3
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB3_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB3 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;
    uint256 airdropAmount;
    uint256 outAmount;
    mathint totalSupplyA;
    
    balanceOfA = TCB3.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    airdropAmount = TCB3.getAirDropAmount(e);
    outAmount = TCB3.getOutAmount(e);
    totalSupplyA = TCB3.totalSupply(e);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;
    require balanceOfA + airdropAmount + airdropAmount+ outAmount+userBalanceOfA < totalSupplyA;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB3.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB3
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB3_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB3 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;
    
    balanceOfA = TCB3.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB3.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB3
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB3_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB3 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    uint256 airdropAmount;
    uint256 outAmount;
    mathint totalSupplyA;
    
    balanceOfA = TCB3.balanceOf(e, currentContract);
    airdropAmount = TCB3.getAirDropAmount(e);
    outAmount = TCB3.getOutAmount(e);
    
    userBalanceOfA = TCB3.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB3.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require balanceOfA + airdropAmount + outAmount + airdropAmount+ userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB3.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB3
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB3_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB3 && getTokenB() == assetB;
    uint256 userBalanceOfLiqidity;
    uint256 userBalanceOfLiqidityAfter;
    uint256 amountAIn;
    uint256 amountBIn;
    uint256 aReserve;
    uint256 bReserve;
    uint256 liquidityTotalSupply;

    aReserve, bReserve = getReserves();
    liquidityTotalSupply = currentContract.totalSupply(e);
    userBalanceOfLiqidity = currentContract.balanceOf(e, e.msg.sender);

    require amountAIn > 0 && amountBIn > 0;
    require liquidityTotalSupply >= aReserve && liquidityTotalSupply >= bReserve; 
    require e.msg.sender != currentContract;
    require userBalanceOfLiqidity == 0;

    currentContract.addLiquidity(e, amountAIn, amountBIn);
    
    userBalanceOfLiqidityAfter = currentContract.balanceOf(e, e.msg.sender);

    assert userBalanceOfLiqidityAfter > 0;
}

//P6_TCB3
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB3_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB3 && getTokenB() == assetB;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;   
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userLiquidityBalance;
    uint256 claimableFeeA;
    uint256 claimableFeeB;
    uint256 claimableFeeAAfter;
    uint256 claimableFeeBAfter;

    require e.msg.sender != currentContract;

    userBalanceOfA = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB3.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB3.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}
