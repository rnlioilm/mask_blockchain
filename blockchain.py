import hashlib
import sys
import time
import json
import logging
import codecs
import base58

from ecdsa import NIST256p
from ecdsa import VerifyingKey
from ecdsa import SigningKey

import core

DIFFICULTY = 3
POINT = 1
MINER = "MINER"
MINER_MYNUMBER = 111111111111

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class BlockChain(object):
    def __init__(self, blockchain_address = None,port = None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0,self.hash({}))
        self.blockchain_address = blockchain_address
        self.port = port

    def create_block(self, nonce, previous_hash):
        block = core.sortedd({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    #def my_num_hash(self,my_number):
    #   return hashlib.sha256((hashlib.sha256(my_number.encode()).hexdigest()).encode()).hexdigest()

    def add_transaction(self, sender_address, recipient_address, value,my_number,place,
                        sender_public_key = None,
                        signature = None):
        #sender_public_key =None,signature =None
        #mn = self.hash(my_number)
        #my_number = self.my_num_hash(str(mynumber))
        transaction = core.sortedd({
            'sender_address': sender_address,
            'recipient_address': recipient_address,
            'value':int(value),
            'my_number':int(my_number),
            'place':place
        })
        if sender_address == MINER:
            self.transaction_pool.append(transaction)
            return True
        if self.varify_transaction(sender_public_key,signature,transaction):
            self.transaction_pool.append(transaction)
            return True
        return False

    def create_transaction(self,  sender_address, recipient_address, value,my_number,place,sender_public_key,signature):

        is_transacted = self.add_transaction(
            sender_address, recipient_address, value,my_number,place,sender_public_key, signature
        )
        return is_transacted


    def varify_transaction(self, sender_public_key, signature, transaction):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        signature_bytes = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(bytes().fromhex(sender_public_key), curve=NIST256p)
        verified_key = verifying_key.verify(signature_bytes, message)
        return verified_key




    def valid(self, transactions, previous_hash, nonce, dif=DIFFICULTY):
        try_block = core.sortedd({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        try_hash = self.hash(try_block)
        return try_hash[:dif] == '0' * dif

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])  # 前のhashを持ってくる
        nonce = 0
        while self.valid(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self):
        self.add_transaction(
            sender_address=MINER,
            recipient_address=self.blockchain_address,
            value=POINT,
            my_number=MINER_MYNUMBER,
            place = "nippon"
        )
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce,previous_hash)
        logger.info({'action': 'mining', 'status': 'success'})
        return True

    def total(self,blockchain_address):
        totals = 0
        for block in self.chain:
            for transaction in block['transactions']:
                value = int(transaction['value'])
                if blockchain_address == transaction['recipient_address']:
                    totals += value
                if blockchain_address == transaction['sender_address']:
                    totals -= value

        return totals





    """
        def mining_total(self,blockchain_address):
        total_amount = 0
        for block in self.chain:
            for transaction in block['z-mining']:
                value = transaction['point']
                if blockchain_address == transaction['Prefecture']:
                    total_amount += value
                if blockchain_address == transaction['MINER']:
                    total_amount -= value
        return total_amount
        
        def mining_transaction(self,sender,recipient,reward):

        transaction = core.sorted_key({
            'sender_address': sender,
            'recipient_address': recipient,
            'value_of_masks': int(reward)
        })
        self.add_transaction(transaction)
        return True
        
        
    """

class Wallet(object):
    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_address()
    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()


    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_address(self):
        """
        If there is an error in the hash and you write the code incorrectly, it's difficult to determine where you made the mistake.
        Please let me know if there was a mistake in my code.

        アウトプットの為、ここの部分がずいぶんと間違っている可能性があります。証明はうまく行っているので大丈夫かと思われます。

        twitter account @rnlioilm
        link https://twitter.com/rnlioilm
        Thanks for your cooperation
        """
        sha256 = (hashlib.sha256(self._public_key.to_string())).digest()#publickey(SHA256)
        ripemed160_s = hashlib.new('ripemd160')
        ripemed160_s.update(sha256)
        ripemed160 = codecs.encode(ripemed160_s.digest(), 'hex')
        nb = b'00' #network byte
        sha256_bpk = hashlib.sha256(codecs.decode(nb + ripemed160,'hex'))#bpk (bitcoin public key)
        sha256_2 = (hashlib.sha256(sha256_bpk.digest())).digest()
        sha256_hex = codecs.encode(sha256_2, 'hex')
        checksum = sha256_hex[:8]
        address_hex = ((nb + ripemed160) + checksum).decode('utf-8')
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address



class Transaction(object):

    def __init__(self, sender_private_key,sender_public_key,
                 sender_address, recipient_address,
                 value,my_number,place):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.value = value
        self.my_number = my_number
        self.place = place

    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = core.sortedd({
            'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'value': int(self.value),
            'my_number':int(self.my_number),
            'place':self.place,
        })
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p)
        private_key_sign = private_key.sign(message)
        signature= private_key_sign.hex()
        return signature