import time
import crypto

class Transaction:

    def __init__(self, sender, key):
        self.sender = sender
        self.key = key

        self.send_to = []
        self.timestamp = time.time()
        self.tip = 0


    def add_receiver(self, receiver, amount):
        self.send_to.append((receiver, amount))


    def set_tip(self, amount):
        if amount < 0:
            return
        else:
            self.tip = amount

    def signing(self):
        msg = bytes(self)
        self.signature = crypto.signing(self.key, msg)

    def __bytes__(self):
        msg = str(self.send_to) + str(self.timestamp) + str(self.tip)
        return self.sender + msg.encode('utf-8')
