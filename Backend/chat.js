const axios = require("axios");

// 确保 API_KEY 正确设置
const API_KEY = ""; // 替换为你的真实 API Key

async function analyzeFailures(failures) {
  const prompt = `
    以下是异常合约/账户检测的日志：
    be initializing..........
use Etherscan API: VGE6P9D2QHCIGVJ1N8E9K5VXQE356HV3NV
input source address:  ['0x6a49f91230311b4823eeb0da26676c45ff41801a']
-------------Start Searching---------------
Contract Creator and Transaction Info: {'contractAddress': '0x6a49f91230311b4823eeb0da26676c45ff41801a', 'creatorAddress': '0x9d828f027848c5b33243e4A556a1934951218aD2', 'txHash': '0x126e9bd277791571a70df94373dc6118ed83b27d7105a0af819a17b3e164f687'}
-------------Collecting related addresses---------------
Total related addresses number: 390
-------------------Few-shot Detection--------------------
the source contract 0x6a49f91230311b4823eeb0da26676c45ff41801a is suspected of [scam token] on 0.3 prediction threshold
----------------Checking Black Accounts List-------------------

Find overlap address from './label/mev.txt' :
0x00000000003b3cc22af3ae1eac0440bcee416b40
0x00000000002d383933aa1609f11d0afa4d5ea90a
0x0000000000d9455cc7eb92d06e00582a982f68fe

Find overlap address from './label/scam.txt' :
0x6a49f91230311b4823eeb0da26676c45ff41801a
--------------Checking Grey Accounts List-------------------

它代表input contract是一个scam token, 并且多个mev bot地址与该合约有交互。这是一个高风险合约，需要进一步调查。

    以下是 Certora 运行的失败日志:${failures};它说明了这个input contract一些代码上对用户资产安全的威胁，假设我是一个不懂技术的普通用户，结合上面的风险提示，量化地评估风险系数，并写一个详细的Markdown报告来解释这个问题，让我(普通用户）能够认识到风险并受到相关安全教育和建议。
    一些代码的检测方式和威胁如下：
    using DummyWeth as assetB;
using TCB5_Reflection as TCB5;

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
}

//P1_TCB5
/**
* @title Prove that after operations the liquidity records in the pool is same or less than the records in the Token contract
* @dev The liquidity records in the pool is same or less than the records in the Token contract
*/
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

  `;

  try {
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions", // 注意API路径
      {
        model: "gpt-4o", // 确保模型名称正确
        messages: [{ role: "user", content: prompt }],
        temperature: 0.7, // 可根据需要调整温度
        max_tokens: 2000,
      },
      {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Error calling ChatGPT API:", error);
    throw new Error("Failed to analyze failures.");
  }
}

module.exports = { analyzeFailures };
