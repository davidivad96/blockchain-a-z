# Create a smart contract

First smart contract created with <a href="https://solidity-es.readthedocs.io/es/latest/">Solidity</a> and deployed to
the <a href="https://ethereum.org/es/">Ethereum</a> blockchain. It's a program that will allow investors to buy
and sell Davidcoins, besides seeing their balance in both, Davidcoins and USD.

## Usage

We will need the following tools:

- <a href="https://remix.ethereum.org/">Remix IDE</a>: it will allow us to compile our smart contract.
- <a href="https://www.trufflesuite.com/ganache">Ganache</a>: so that we can have our test accounts with some fake
  Ethers and be able to record all the blocks and transactions added to the blockchain.
- <a href="https://metamask.io/">Metamask</a>: browser extension that will act as a crypto wallet and gateway to
  our blockchain app.
- <a href="https://www.myetherwallet.com/">MyEtherWallet</a>: web/mobile app that will let us to deploy and interact
  with our smart contract.
  
So the first thing we need to do is download and install Ganache. Open it and create a new workspace. You now can see
a blockchain with only the genesis block, and some test accounts with 100 Ethers each.

Next, we will go to the Metamask extension and import a new account. You can choose any account from Ganache, copy its
private key and add it to Metamask. This is the account we will be using to interact with the smart contract.

Then, go to MyEtherWallet and click on "Access My Wallet". It will give you multiple options. We will select "MEW CX",
which will allow us to access our Metamask wallet.

Once we are inside the MyEtherWallet dashboard, go to the section "Contract" and click on "Deploy Contract". It will
ask you for the Byte Code, ABI/JSON Interface, and the Contract Name. To have this data, just go to the Remix IDE,
compile the contract and click on "Compilation Details". There you will be able to copy the ABI and the BYTECODE. For
the Bytecode, remember to copy only the large number in the "object" key. And, when you are going to paste this number
in MyEtherWallet, bear in mind that maybe you have to add a "0x" just in the beginning of the Bytecode.

Finally, if everything has gone well, click on "Sign Transaction" and confirm the transaction in Metamask. Your
contract has been deployed, and now you can interact with it from MyEtherWallet. You can also see in Ganache that
a new block has been added with the transaction to deploy the smart contract. There it is the contract address that
we need to specify in MyEtherWallet to access the contract.
