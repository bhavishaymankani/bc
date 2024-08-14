import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self):
        random_gen = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random_gen)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time
        })

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

def display_transaction(transaction):
    dict_txn = transaction.to_dict()
    print("sender: " + dict_txn['sender'])
    print(' ---- ')
    print("recipient: " + dict_txn['recipient'])
    print(' ---- ')
    print("value: " + str(dict_txn['value']))
    print(' ---- ')
    print("time: " + str(dict_txn['time']))
    print(' ---- ')

class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""

def dump_blockchain(blockchain):
    print("Number of blocks in the chain: " + str(len(blockchain)))
    for x in range(len(blockchain)):
        block_temp = blockchain[x]
        print("block # " + str(x))
        for transaction in block_temp.verified_transactions:
            display_transaction(transaction)
        print(' ')
        print('=====================================')

# Example Usage
Dinesh = Client()
t0 = Transaction("Genesis", Dinesh.identity, 500.0)
block0 = Block()
block0.previous_block_hash = None
block0.Nonce = None
block0.verified_transactions.append(t0)

# Hashing the block
digest = hash(block0)
last_block_hash = digest

TPCoins = []
TPCoins.append(block0)

# Dump the blockchain
dump_blockchain(TPCoins)
