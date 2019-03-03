from block import Block
from flask import Flask, jsonify, request
from transaction import Transaction
import crypto
import utils
from cryptography.hazmat.primitives.asymmetric import rsa

class Blockchain:

    def __init__(self, last_block = None):
        self.last_block = last_block


    def set_last_block(self, last_block):
        self.last_block = last_block


    def __len__(self):
        n = 0
        block = self.last_block
        while(isinstance(block, Block)):
            n += 1
            block = block.prev_block
        return n

# Instantiate the Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

msg = b'hello, world'
key = crypto.loadKey('key.pem')
isinstance(key, rsa.RSAPrivateKey)
signature = crypto.signing(key, msg)
crypto.verification(key.public_key(), msg, signature)
addr = crypto.genAddr(key.public_key())
block = Block(addr, key)

@app.route('/mine', methods=['GET'])
def mine():
    global block
    if block.transactions:
        print("Block: ", block.transactions)
        print("blockchain.last_block", blockchain.last_block)
        block.prev_block = blockchain.last_block
        print(str(block))
        blockchain.last_block = block
        print("blockchain.last_block", blockchain.last_block)

        block.build_merkle_tree()
        block.proofOfWork()
    block = Block(addr, key)

    return jsonify({"Status":"Success"}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'voteGroup']
    if not all(k in values for k in required):
        return 'Missing values', 400

    t = Transaction(values['sender'])
    t.set_tip(0.5)
    t.add_receiver(values['sender'], values['voteGroup'])
    t.signing(key)

    block.add_transaction(t)
    print("Block: ", block.transactions)

    crypto.verification(key.public_key(), bytes(t), t.signature)

    response = {'message': f'Transaction will be added to Block'}
    return jsonify(response), 201

@app.route('/votesummary', methods=['GET'])
def vote_summary():
    #Counts all votes that have been added to the blockchain via successful transactions
    #Returns a JSON response with voting parties and their respective vote-counts so far
    block_iter = blockchain.last_block
    dict_votes = {}
    print("Block: ", block_iter.transactions)
    while block_iter != None:
        print("Block: ", block_iter.transactions)
        for tr in block_iter.transactions:
            print(tr.send_to)
            if tr.send_to[0][1] not in dict_votes:
                dict_votes[tr.send_to[0][1]] = 1
            else:
                dict_votes[tr.send_to[0][1]] += 1
        block_iter = block_iter.prev_block

    return jsonify(dict_votes), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
