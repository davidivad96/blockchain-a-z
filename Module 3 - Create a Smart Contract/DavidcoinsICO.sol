// Davidcoins ICO

// Version of compiler
pragma solidity ^0.8.2;

contract DavidcoinsICO {
  // Introducing the maximum number of Davidcoins available for sale
  uint public max_davidcoins = 1000000;

  // Introducing the USD to Davidcoins conversion rate
  uint public usd_to_davidcoins = 1000;

  // Introducing the total number of Davidcoins that have been bought by the investors
  uint public total_davidcoins_bought = 0;

  // Mapping from the investor address to its equity in Davidcoins and USD
  mapping(address => uint) equity_davidcoins;
  mapping(address => uint) equity_usd;

  // Checking if an investor can buy Davidcoins
  modifier can_buy_davidcoins(uint usd_invested) {
    require(usd_invested * usd_to_davidcoins + total_davidcoins_bought < max_davidcoins);
    _;
  }

  // Getting the equity in Davidcoins of an investor
  function equity_in_davidcoin(address investor) external view returns (uint) {
    return equity_davidcoins[investor];
  }

  // Getting the equity in USD of an investor
  function equity_in_usd(address investor) external view returns (uint) {
    return equity_usd[investor];
  }

  // Buying Davidcoins
  function buy_davidcoins(address investor, uint usd_invested) external can_buy_davidcoins(usd_invested) {
    uint davidcoins_bought = usd_invested * usd_to_davidcoins;
    equity_davidcoins[investor] += davidcoins_bought;
    equity_usd[investor] = equity_davidcoins[investor] / usd_to_davidcoins;
    total_davidcoins_bought += davidcoins_bought;
  }

  // Selling Davidcoins
  function sell_davidcoins(address investor, uint davidcoins_sold) external {
    equity_davidcoins[investor] -= davidcoins_sold;
    equity_usd[investor] = equity_davidcoins[investor] / usd_to_davidcoins;
    total_davidcoins_bought -= davidcoins_sold;
  }
}
