#pip install bitcoinlib
#  #Use Python 3.9.12
from bitcoinlib.wallets import Wallet 
w = Wallet.create('Wallet3')
key1 = w.get_key() 
print(key1.address)
# Send a small transaction to your wallet and use the scan() method to update transactions and UTXO’s
w.scan()
print(w.info())