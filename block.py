import time
import crypto
import utils

LEADING_ZEROS = 1


class Block:

    def __init__(self, miner, key):
        self.miner = miner
        self.key = key

        self.transactions = []
        self.timestamp = utils.getTimestamp()


    def add_transaction(self, transaction):
        self.transactions.append(transaction)


    def build_merkle_tree(self):
        n = 1
        while(n < len(transactions)):   n *= 2

        merkle = [b'\x00'] * (2*n)
        for i in range(len(transactions)):
            data = bytes(transactions[i]) + transactions[i].signature
            merkle[n+i] = crypto.dhash(data)

        for i in reversed(range(1, n)):
            merkle[i] = crypto.dhash(merkle[2*i] + merkle[2*i+1])

        self.merkle_tree = merkle


    def proofOfWork(self):
        data = bytes(self)
        nonce = 0

        while(True):
            nonce_b = nonce.to_bytes(16, byteorder = 'big')
            res = dhash(data + nonce_b)
            if int.from_bytes(res[:LEADING_ZEROS], byteorder = 'big') == 0:
                self.nonce = nonce
                return


    def signing(self):
        msg = bytes(self) + self.nonce.to_bytes(16, byteorder = 'big')
        self.signature = crypto.signing(self.key, msg)


    def __bytes__(self):
        data = self.miner
        for t in transactions:  data += bytes(t) + t.signature
        data += str(timestamp).encode('utf-8')
        for m in merkle_tree:   data += m
        return data
