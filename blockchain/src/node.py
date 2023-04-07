import hashlib
import random
import time
from blockchain.src.block import Block
import json
from datetime import datetime


class Node:
    def __init__(self, process):
        self.process = process  # Node id
        self.chain = []  # Chain of blocks
        self.last_block = None
        self.difficulty = 4  # Difficulty for hash

    # Creates new block
    def create_new_block(self):
        index = self.last_block.index + 1  # index of new block
        prev_hash = self.last_block.hash_  # prev_hash of new block
        data = self.get_data()  # data of new block
        nonce = 0  # nonce of new block
        hash_ = self.get_hash(index, prev_hash, data, nonce)  # hash of new block
        block = Block(
            index=index,
            prev_hash=prev_hash,
            data=data,
            nonce=nonce,
            hash_=hash_,
            time=None
        )
        # Block mining
        mined_block = self.mine(block)
        return mined_block

    # Generate data - a string of random 256 characters
    @staticmethod
    def get_data():
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        data = ''.join(random.choice(letters) for _ in range(256))
        return data

    # Generate hash from index, prev_hash, data, nonce
    @staticmethod
    def get_hash(index: int, prev_hash: str, data: str, nonce: int):
        h = hashlib.sha256(f"{index}{prev_hash}{data}{nonce}".encode('utf-8')).hexdigest()
        return h

    # Mining a block to the correct hash
    def mine(self, block):
        while block.hash_[-self.difficulty:] != '0' * self.difficulty:
            # Different nonce change for different Nodes
            if self.process.id == 1:
                block.nonce += 1
            elif self.process.id == 2:
                block.nonce += 5
            else:
                block.nonce += random.randint(1, 25)
            block.hash_ = self.get_hash(block.index, block.prev_hash, block.data, block.nonce)
        return Block(block.index, block.prev_hash, block.hash_, block.data, block.nonce, datetime.now().time())

    # Received block handler
    def handle_received_block(self, received_block):
        # Convert received block to Python object
        block_in_json = json.loads(received_block)
        # Convert Python object to Block
        block = Block.block_from_json(block_in_json)

        # If genesis, appends to chain
        if block.index == 0:
            self.chain.append(block)
            self.last_block = block
            block.print_block(0, True)
            return True

        self_last_block_index = 0
        if self.last_block is not None:
            self_last_block_index = self.last_block.index
        # If block is valid, appends to chain

        if block.index == self_last_block_index + 1:
            self.chain.append(block)
            self.last_block = block
            block.print_block(int(block_in_json['node_num']), False)
            return True

        # If node added its block to chain and broadcast it, but than received a new block with same index
        # so check by timestamp
        if block.index == self_last_block_index and block.timestamp < self.last_block.timestamp:
            self.chain[-1] = block
            self.last_block = block
            block.print_block(int(block_in_json['node_num']), False)
            time.sleep(1)
            return True
        return False

    # Creates genesis block
    def create_genesis(self):
        genesis = Block(
            0,
            "GENESIS",
            "hash",
            "data",
            0,
            datetime.now().time()
        )
        self.chain.append(genesis)
        self.last_block = genesis
        genesis.print_block(1, True)
        return genesis

    # Checking the correctness of the chain
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            current_block_hash = self.get_hash(current_block.index, current_block.prev_hash,
                                               current_block.data, current_block.nonce)

            if current_block.hash_ != current_block_hash or prev_block.hash_ != current_block.prev_hash:
                return False
        return True

    # Converts chain to string
    def chain_to_string(self, length):
        str_chain = ""
        for i in range(length):
            block = self.chain[i]
            str_chain += f"Block(index={block.index}, prev_hash={block.prev_hash}, hash={block.hash_}, " \
                         f"data={block.data}, nonce={block.nonce}, timestamp={block.timestamp}) \n"

        return str_chain
