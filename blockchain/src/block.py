

class Block:
    def __init__(self, index: int, prev_hash: str, hash_: str, data: str, nonce: int):
        self.index = index  # the block number, increase in order from the first
        self.prev_hash = prev_hash  # the hash of the previous block
        self.hash_ = hash_  # hash of the current block
        self.data = data  # data, in our case it is a string of random 256 characters
        self.nonce = nonce  # an addition to the hash requirement.




