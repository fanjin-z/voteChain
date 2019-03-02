from block import Block

class Blockchain:

    def __init__(self, last_block):
        self.last_block = last_block


    def set_last_block(last_block):
        self.last_block = last_block


    def __len__(self):
        n = 0
        block = self.last_block
        while(isinstance(block, Block)):
            n += 1
            block = block.prev_block
        return n
