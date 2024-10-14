pragma solidity >= 0.8.0;

import "../../contracts/Token/FlashMint.sol";
import "../../contracts/Swap/ISwap.sol";
import "../helpers/ArbitraryValues.sol";

/**
 * A flexible implementation of the FlashLoanReceiver callback that
 * nondeterministically makes calls back to the token.
 */
contract FlexibleReceiver is IFlashMintReceiver, ArbitraryValues {

    ISimpleSwap Swap;
    /**
     * Nondeterministically call {deposit}, {transferFrom}, {withdraw},
     * {transfer}, or {approve} on the {token}.
     *
     * @return true
     */
    function executeOperation(
        uint256 amount,
        uint256 premium,
        address initiator
    ) external override(IFlashMintReceiver) returns (bool) {
        uint  callbackChoice = arbitraryUint();
        if (callbackChoice == 0)
            Swap.swap(arbitraryAddress(), arbitraryAddress(), arbitraryUint());
        else if (callbackChoice == 1)
            Swap.addLiquidity(arbitraryUint(),arbitraryUint());
        else if (callbackChoice == 2)
            Swap.removeLiquidity(arbitraryUint());
        // else if (callbackChoice == 3)
        //     Swap.transfer(arbitraryAddress(),arbitraryUint());
        // else if (callbackChoice == 4)
        //     Swap.approve(arbitraryAddress(),arbitraryUint());

        return true;
    }
}
