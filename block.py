import time


class Block:

    def __init__(self, miner, key):
        self.miner = miner
        self.key = key

        self.transactions = []
        self.timestamp = time.time()
        self.merkle_tree = []


    def add_transaction(self, transaction):
        self.transactions.append(transaction)


    def build_merkle_tree(self):
        pass


    def proofOfWork(self):
        pass


    def __bytes__(self):
        pass 
        # data = str(self.miner) +
