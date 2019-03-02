import time

class Transaction:

    def __init__(self, sender):
        self.sender = sender
        self.send_to = []
        self.timestamp = time.time()
        self.tip = 0


    def add_receiver(receiver, amount):
        self.send_to.append((receiver, amount))


    def add_tip(amount):
        if amount < 0:
            return
        else:
            self.tip = amount

    def sign(self):
        pass
