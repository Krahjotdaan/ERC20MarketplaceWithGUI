from web3 import Web3, HTTPProvider


PROVIDER = "https://holesky.infura.io/v3/69f2d3f6cfc84b92a29e3f3bd1b4ec8b"
WALLET_ADDRESS = ""
PRIVATE_KEY = ""
marketplace = "0x83057dbC72018Be1740A4f42f0d704DE7FDE59cb"

true = True
false = False

PRINT_EVENT = True

MARKETPLACE_ABI = [{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Cancel","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"oldPrice","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"newPrice","type":"uint256"}],"name":"ChangePrice","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":true,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ListLot","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"lotId","type":"uint256"},{"indexed":false,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":true,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"customer","type":"address"}],"name":"Purchase","type":"event"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"cancel","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"newPrice","type":"uint256"}],"name":"changePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"list","outputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddress","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"listLot","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"lotId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"purchase","outputs":[],"stateMutability":"payable","type":"function"}]

W3 = Web3(HTTPProvider(PROVIDER))

MARKETPLACE = W3.eth.contract(address=marketplace, abi=MARKETPLACE_ABI)
