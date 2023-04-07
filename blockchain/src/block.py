import json
from datetime import datetime


class Block:
    def __init__(self, index: int, prev_hash: str, hash_: str, data: str, nonce: int, time):
        self.index = index  # the block number, increase in order from the first
        self.prev_hash = prev_hash  # the hash of the previous block
        self.hash_ = hash_  # hash of the current block
        self.data = data  # data, in our case it is a string of random 256 characters
        self.nonce = nonce  # an addition to the hash requirement.
        self.timestamp = time

    # Converts Block to JSON
    def block_to_json(self, process_id):
        block_to_dict = {
            "node_num": process_id,
            "index": self.index,
            "prev_hash": self.prev_hash,
            "hash_": self.hash_,
            "data": self.data,
            "nonce": self.nonce,
            "time": str(self.timestamp)
        }
        return json.dumps(block_to_dict)

    # Converts JSON to Block
    @staticmethod
    def block_from_json(block_dict):
        dict_to_block = Block(
            int(block_dict['index']),
            block_dict['prev_hash'],
            block_dict['hash_'],
            block_dict['data'],
            int(block_dict['nonce']),
            datetime.strptime(block_dict['time'], '%H:%M:%S.%f').time()
        )
        return dict_to_block

    # Prints Block to console
    def print_block(self, process_id, flag):
        block_str = f"Block(index={self.index}, prev_hash={self.prev_hash}, hash={self.hash_}, data={self.data}, " \
                    f"nonce={self.nonce}, timestamp={self.timestamp})"
        if flag:
            print(f"Initialized GENESIS:  {block_str}")
        else:
            print(f"Received block from Node {process_id}:  {block_str}")

