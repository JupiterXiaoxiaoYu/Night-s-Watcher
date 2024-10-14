using DummyWeth as assetB;
using ERC20 as TCB0;
using TCB1_Rebasing as TCB1;
using TCB2_Deflation as TCB2;
using TCB3_Inflation_Airdrop as TCB3;
using TCB4_Fee as TCB4;
using TCB5_Reflection as TCB5;
using TCB6_FrontRunSwap as TCB6;
using TCB7_FrontRunAddLiq as TCB7;
using TCB8_Frozen as TCB8;
using TCB9_Pause as TCB9;
using TCB10_FlashMint as TCB10;

// using ERC20 as assetC;

methods
{
    function swap(address, address, uint256) external returns(uint256);
    function getTokenA() external returns(address) envfree;
    function getTokenB() external returns(address) envfree;
    function getReserves() external returns(uint256, uint256) envfree;
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.getGonsPerFragment() external => DISPATCHER(true);
    function _.getAirDropAmount() external => DISPATCHER(true);
    function _.getOutAmount() external => DISPATCHER(true);
    function _.isInitialized(address) external => DISPATCHER(true);
    function _.getSwapAddress() external => DISPATCHER(true);
    function _.getSwapPercentage() external => DISPATCHER(true);
    function _.blockUser(address) external => DISPATCHER(true);
    function _.allow(address) external => DISPATCHER(true);
    function _.stop() external => DISPATCHER(true);
    function _.start() external => DISPATCHER(true);
    function _.flashMint(address, uint256) external => DISPATCHER(true);
}

//P1_TCB0
/**
* @title Prove that after operations the liquidity records in the pool is same or less than the records in the Token contract
* @dev The liquidity records in the pool is same or less than the records in the Token contract
*/
rule TCB0_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB0 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB0.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB0.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB0
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB0_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB0 && getTokenB() == assetB;

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
    
    balanceOfA = TCB0.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB0.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB0
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB0_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB0 && getTokenB() == assetB;

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
    
    balanceOfA = TCB0.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB0.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB0
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB0_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB0 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB0.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB0.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB0.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB0.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB0
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB0_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB0 && getTokenB() == assetB;
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

//P6_TCB0
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB0_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB0 && getTokenB() == assetB;
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

    userBalanceOfA = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB0.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB0.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

//P1_TCB1
/**
* @title Prove that after operations the liquidity records in the pool is same or less than the records in the Token contract
* @dev The liquidity records in the pool is same or less than the records in the Token contract
*/
rule TCB1_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB1 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB1.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB1.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB1
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB1_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB1 && getTokenB() == assetB;

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
    
    balanceOfA = TCB1.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB1.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB1
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB1_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB1 && getTokenB() == assetB;

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
    
    balanceOfA = TCB1.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB1.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB1
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB1_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB1 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    uint256 gonsPerFragment;
    mathint totalSupplyA;

    gonsPerFragment = TCB1.getGonsPerFragment(e);
    balanceOfA = TCB1.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB1.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB1.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB1.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB1
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB1_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB1 && getTokenB() == assetB;
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

//P6_TCB1
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB1_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB1 && getTokenB() == assetB;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;   
    uint256 userLiquidityBalance;
    uint256 claimableFeeA;
    uint256 claimableFeeB;
    uint256 claimableFeeAAfter;
    uint256 claimableFeeBAfter;

    require e.msg.sender != currentContract;

    userBalanceOfA = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0 && claimableFeeA > 0 && claimableFeeB > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB1.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB2_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB2 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB2.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB2.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB2
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB2_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB2 && getTokenB() == assetB;

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
    balanceOfA = TCB2.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB2.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB2
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB2_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB2 && getTokenB() == assetB;

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
    
    balanceOfA = TCB2.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB2.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB2
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB2_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB2 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB2.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB2.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB2.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB2.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB2
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB2_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB2 && getTokenB() == assetB;
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

//P6_TCB2
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB2_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB2 && getTokenB() == assetB;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;   
    uint256 userLiquidityBalance;
    uint256 claimableFeeA;
    uint256 claimableFeeB;
    uint256 claimableFeeAAfter;
    uint256 claimableFeeBAfter;

    require e.msg.sender != currentContract;

    userBalanceOfA = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0 && claimableFeeA > 0 && claimableFeeB > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB2.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

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

rule TCB4_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB4 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB4.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB4.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB4
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB4_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB4 && getTokenB() == assetB;

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
    
    balanceOfA = TCB4.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB4.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB4
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB4_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB4 && getTokenB() == assetB;

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
    
    balanceOfA = TCB4.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB4.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB4
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB4_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB4 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB4.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB4.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB4.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB4.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB4
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB4_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB4 && getTokenB() == assetB;
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

//P6_TCB4
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB4_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB4 && getTokenB() == assetB;
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

    userBalanceOfA = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB4.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB4.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB5_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB5 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB5.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB5.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB5
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB5_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB5 && getTokenB() == assetB;

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
    
    balanceOfA = TCB5.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB5.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB5
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB5_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB5 && getTokenB() == assetB;

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
    
    balanceOfA = TCB5.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB5.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB5
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB5_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB5 && getTokenB() == assetB;

    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB5.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB5.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB5.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB5.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB5
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB5_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB5 && getTokenB() == assetB;
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

//P6_TCB5
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB5_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB5 && getTokenB() == assetB;
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

    userBalanceOfA = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB5.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB5.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB6_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 swapPercentage;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

    aReserve, bReserve = getReserves();
    balanceOfA = TCB6.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB6.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB6
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB6_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;

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
    uint256 swapPercentage;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;
    
    balanceOfA = TCB6.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB6.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB6
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB6_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 userBalanceOfA;
    uint256 userBalanceOfB;
    uint256 userBalanceOfAAfter;
    uint256 userBalanceOfBAfter;
    uint256 swapPercentage;
    uint256 userLiquidityBalance;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

    aReserve, bReserve = getReserves();
    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);
    require userLiquidityBalance > 0;
    
    balanceOfA = TCB6.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB6.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB6
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB6_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    uint256 swapPercentage;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;
    
    balanceOfA = TCB6.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB6.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB6.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB6.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB6
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB6_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;
    uint256 userBalanceOfLiqidity;
    uint256 userBalanceOfLiqidityAfter;
    uint256 amountAIn;
    uint256 amountBIn;
    uint256 aReserve;
    uint256 bReserve;
    uint256 liquidityTotalSupply;
    uint256 swapPercentage;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

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

//P6_TCB6
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB6_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB6 && getTokenB() == assetB && TCB6.getSwapAddress(e) == currentContract;
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
    uint256 swapPercentage;
    swapPercentage = TCB6.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

    require e.msg.sender != currentContract;

    userBalanceOfA = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB6.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB6.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB7_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

    aReserve, bReserve = getReserves();
    balanceOfA = TCB7.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB7.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB7
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB7_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;

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
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;
    
    balanceOfA = TCB7.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB7.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB7
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB7_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;

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
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;
    
    balanceOfA = TCB7.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB7.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB7
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB7_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;
    
    balanceOfA = TCB7.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB7.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB7.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB7.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB7
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB7_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;
    uint256 userBalanceOfLiqidity;
    uint256 userBalanceOfLiqidityAfter;
    uint256 amountAIn;
    uint256 amountBIn;
    uint256 aReserve;
    uint256 bReserve;
    uint256 liquidityTotalSupply;
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

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

//P6_TCB7
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB7_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB7 && getTokenB() == assetB && TCB7.getSwapAddress(e) == currentContract;
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
    uint256 swapPercentage;
    swapPercentage = TCB7.getSwapPercentage(e);
    require swapPercentage > 0 && swapPercentage < 100;

    require e.msg.sender != currentContract;

    userBalanceOfA = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB7.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB7.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB8_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB8 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB8.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB8.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB8
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB8_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB8 && getTokenB() == assetB;

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
    
    balanceOfA = TCB8.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB8.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB8
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB8_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB8 && getTokenB() == assetB;

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
    
    balanceOfA = TCB8.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB8.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB8
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB8_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB8 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB8.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB8.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB8.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB8.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB8
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB8_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB8 && getTokenB() == assetB;
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

//P6_TCB8
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB8_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB8 && getTokenB() == assetB;
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

    userBalanceOfA = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB8.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB8.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

rule TCB9_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB9 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB9.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB9.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB9
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB9_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB9 && getTokenB() == assetB;

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
    
    balanceOfA = TCB9.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB9.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB9
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB9_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB9 && getTokenB() == assetB;

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
    
    balanceOfA = TCB9.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB9.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB9
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB9_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB9 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB9.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB9.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB9.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB9.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB9
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB9_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB9 && getTokenB() == assetB;
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

//P6_TCB9
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB9_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB9 && getTokenB() == assetB;
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

    userBalanceOfA = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB9.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB9.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;

    
}

rule TCB10_PoolLiquidityRecordsIsSameOrLessThanTokenContractLiquidityRecords(method f) filtered {f -> !f.isView && f.selector!=sig:claimFee().selector} {
    env e;
    calldataarg args;
    require getTokenA() == TCB10 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 aReserveAfter;
    uint256 bReserveAfter;
    uint256 balanceOfAAfter;
    uint256 balanceOfBAfter;
    
    aReserve, bReserve = getReserves();
    balanceOfA = TCB10.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.f(e,args);
    
    aReserveAfter, bReserveAfter = getReserves();
    balanceOfAAfter = TCB10.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    assert aReserveAfter <= balanceOfAAfter && bReserveAfter <= balanceOfBAfter,
    "The liquidity records in the pool is same or less than the records in the Token contract";
}


//P2_TCB1
/**
* @title Prove that after operations the liquidity / token gained by users is same or more than the pool has transferred
* @dev The liquidity / token gained by users is same or more than the pool has transferred
*/
rule TCB10_PoolTokenGainedByUsersSwappingIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB10 && getTokenB() == assetB;

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
    
    balanceOfA = TCB10.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    aReserve, bReserve = getReserves();
    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.swap(e,args);
    
    balanceOfAAfter = TCB10.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The liquidity / token gained by users is same or more than the pool has transferred";
}

//P3_TCB1
/**
* @title Prove that after operations the token gained by users removing liquidity is same or more than the pool has transferred
* @dev The token gained by users removing liquidity is same or more than the pool has transferred
*/

rule TCB10_PoolTokenGainedByUsersRemovingLiquidityIsSameOrMoreThanPoolTransferred(method f) filtered {f -> !f.isView} {
    env e;
    calldataarg args;
    require getTokenA() == TCB10 && getTokenB() == assetB;

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
    
    balanceOfA = TCB10.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    userBalanceOfA = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    require balanceOfA >= aReserve && balanceOfB >= bReserve && aReserve > 0 && bReserve > 0;

    require e.msg.sender != currentContract;
    currentContract.removeLiquidity(e,args);
    
    balanceOfAAfter = TCB10.balanceOf(e, currentContract);
    balanceOfBAfter = assetB.balanceOf(e, currentContract);

    userBalanceOfAAfter = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    assert (balanceOfA - balanceOfAAfter) <= (userBalanceOfAAfter - userBalanceOfA) && (balanceOfB - balanceOfBAfter) <= (userBalanceOfBAfter - userBalanceOfB),
    "The token gained by users removing liquidity is same or more than the pool has transferred";
}


//P4_TCB1
/**
* @title Prove that after operations the liquidity in the pool is always available - can be swapped
* @dev The liquidity in the pool is always available - can be swapped
*/
rule TCB10_PoolLiquidityIsAlwaysAvailable{
    env e;
    env e1;
    require getTokenA() == TCB10 && getTokenB() == assetB;

    uint256 aReserve;
    uint256 bReserve;
    uint256 balanceOfA;
    uint256 balanceOfB;
    uint256 userBalanceOfA;
    mathint totalSupplyA;
    
    balanceOfA = TCB10.balanceOf(e, currentContract);
    
    userBalanceOfA = TCB10.balanceOf(e, e1.msg.sender);
    totalSupplyA = TCB10.totalSupply(e);

    require balanceOfA > 0 && userBalanceOfA > 0 && balanceOfA + userBalanceOfA < totalSupplyA;
    require e.msg.sender != e1.msg.sender;
    require e.msg.sender == currentContract;
    TCB10.transferFrom@withrevert(e, e.msg.sender, e1.msg.sender, balanceOfA);

    assert !lastReverted,
    "The liquidity in the pool is always available - can be swapped";
}

//P5_TCB1
/**
* @title Prove that after adding liquidity the liquidity records the liquidity balance of user is more than 0
* @dev The liquidity records the liquidity balance of user is more than 0
*/
rule TCB10_PoolLiquidityRecordsTheLiquidityBalanceOfUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB10 && getTokenB() == assetB;
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

//P6_TCB1
/**
* @title Prove that the fee gained by the user is more than 0
* @dev The fee gained by the user is more than 0
*/
rule TCB10_PoolFeeGainedByUserIsMoreThan0() {
    env e;
    require getTokenA() == TCB10 && getTokenB() == assetB;
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

    userBalanceOfA = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfB = assetB.balanceOf(e, e.msg.sender);

    balanceOfA = TCB10.balanceOf(e, currentContract);
    balanceOfB = assetB.balanceOf(e, currentContract);

    claimableFeeA = currentContract.getClaimableFeeA(e);
    claimableFeeB = currentContract.getClaimableFeeB(e);

    require balanceOfA>claimableFeeA && balanceOfB>claimableFeeB && claimableFeeA > 0 && claimableFeeB > 0;

    userLiquidityBalance = currentContract.balanceOf(e, e.msg.sender);

    require userBalanceOfA == 0 && userBalanceOfB == 0 && userLiquidityBalance > 0;

    currentContract.claimFee(e);
    
    userBalanceOfAAfter = TCB10.balanceOf(e, e.msg.sender);
    userBalanceOfBAfter = assetB.balanceOf(e, e.msg.sender);

    claimableFeeAAfter = currentContract.getClaimableFeeA(e);
    claimableFeeBAfter = currentContract.getClaimableFeeB(e);

    assert userBalanceOfAAfter > 0 && userBalanceOfBAfter > 0;
    assert claimableFeeAAfter == 0 && claimableFeeBAfter == 0;
}

