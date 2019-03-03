import time
import crypto
import utils
from transaction import Transaction

LEADING_ZEROS = 2


class Block:

    def __init__(self, miner, key, prev_block=None):
        self.miner = miner
        self.key = key

        self.prev_block = prev_block
        try:
            self.prev_hash = prev_hash.merkle_tree[1]
        except:
            self.prev_hash = b'\x00'

        self.transactions = []
        self.timestamp = utils.getTimestamp()


    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.transactions.append(transaction)


    def build_merkle_tree(self, isreturn=False):
        n = 1
        while(n < len(self.transactions)):   n *= 2

        merkle = [b'\x00'] * (2*n)
        for i in range(len(self.transactions)):
            data = bytes(self.transactions[i]) + self.transactions[i].signature
            merkle[n+i] = crypto.dhash(data)

        for i in reversed(range(1, n)):
            merkle[i] = crypto.dhash(merkle[2*i] + merkle[2*i+1])

        if isreturn:
            return merkle
        else:
            self.merkle_tree = merkle


    def proofOfWork(self, isreturn=False):
        data = bytes(self)
        nonce = 0

        while(True):
            nonce_b = nonce.to_bytes(16, byteorder = 'big')
            res = crypto.dhash(data + nonce_b)
            if int.from_bytes(res[:LEADING_ZEROS], byteorder = 'big') == 0:
                if isreturn:
                    return nonce
                else:
                    self.nonce = nonce
                    # print(nonce)
                    return
            nonce += 1


    def signing(self):
        msg = bytes(self) + self.nonce.to_bytes(16, byteorder = 'big')
        self.signature = crypto.signing(self.key, msg)


    def __bytes__(self):
        data = self.miner
        data += self.prev_hash
        for t in self.transactions:  data += bytes(t) + t.signature
        data += str(self.timestamp).encode('utf-8')
        for m in self.merkle_tree:   data += m
        return data
