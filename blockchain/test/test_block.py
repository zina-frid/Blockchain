import hashlib
import json
import random
from datetime import datetime
from blockchain.src.block import Block


def test_json_convert():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    for i in range(100):
        index = random.randint(1, 20)
        prev_hash = ''.join(random.choice(letters) for _ in range(16))
        data = ''.join(random.choice(letters) for _ in range(256))
        nonce = random.randint(1, 200)
        hash_ = hashlib.sha256(f"{index}{prev_hash}{data}{nonce}".encode('utf-8')).hexdigest()

        b_before = Block(index, prev_hash, hash_, data, nonce, datetime.now().time())
        b_json = b_before.block_to_json(1)
        b_after = Block.block_from_json(json.loads(b_json))

        assert b_before.index == b_after.index and b_before.prev_hash == b_after.prev_hash
        assert b_before.hash_ == b_after.hash_ and b_before.data == b_after.data
        assert b_before.nonce == b_after.nonce and b_before.timestamp == b_after.timestamp




