import random
from datetime import datetime
from blockchain.src.block import Block
from blockchain.src.node import Node
from blockchain.src.main import Process
import pytest


def gen_block_attributes():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    index = random.randint(1, 20)
    prev_hash = ''.join(random.choice(letters) for _ in range(16))
    data = ''.join(random.choice(letters) for _ in range(256))
    nonce = random.randint(1, 200)
    return index, prev_hash, data, nonce


def test_genesis():
    node = Node(1)
    genesis = node.create_genesis()
    assert len(node.chain) == 1
    assert node.last_block == genesis and node.last_block is not None
    assert node.chain[0].index == 0 and node.chain[0].prev_hash == "GENESIS"
    assert node.last_block == node.chain[-1]


def test_get_data():
    for i in range(100):
        assert len(Node.get_data()) == 256


def test_get_hash():
    for i in range(100):
        index, prev_hash, data, nonce = gen_block_attributes()
        old_hash = Node.get_hash(index, prev_hash, data, nonce)
        data += 'change'
        new_hash = Node.get_hash(index, prev_hash, data, nonce)
        assert old_hash != new_hash


@pytest.mark.parametrize('port_num', [8001, 8002, 8003])
def test_mine(port_num):
    for i in range(100):
        process = Process(port_num)
        index, prev_hash, data, nonce = gen_block_attributes()
        hash_ = Node.get_hash(index, prev_hash, data, nonce)
        block = Block(index, prev_hash, data, hash_, nonce, None)
        mined_block = process.node.mine(block)
        assert mined_block.hash_[-4:] == '0000'


@pytest.mark.parametrize('port_num', [8001, 8002, 8003])
def test_create_new_block(port_num):
    process = Process(port_num)
    process.node.create_genesis()
    for i in range(100):
        block = process.node.create_new_block()
        process.node.chain.append(block)
        process.node.last_block = block

    for i in range(1, len(process.node.chain)):
        current_block = process.node.chain[i]
        prev_block = process.node.chain[i - 1]
        current_block_hash = process.node.get_hash(current_block.index, current_block.prev_hash,
                                                   current_block.data, current_block.nonce)

        assert current_block.hash_ == current_block_hash
        assert prev_block.hash_ == current_block.prev_hash


@pytest.mark.parametrize('port_num', [8001, 8002, 8003])
def test_handle_received_block(port_num):
    process = Process(port_num)
    genesis = Block(0, "GENESIS", "hash", "data", 0, datetime.now().time()).block_to_json(process.id)
    res = process.node.handle_received_block(genesis)

    assert len(process.node.chain) == 1 and process.node.last_block is not None
    assert res is True

    ports = [8001, 8002, 8003]
    for i in range(100):
        port = random.choice(ports)
        new_block = process.node.create_new_block()
        # imitate that we generate block or received it
        if port == port_num:
            process.node.chain.append(new_block)
            process.node.last_block = new_block
        else:
            block_to_json = new_block.block_to_json(port)
            res = process.node.handle_received_block(block_to_json)

            assert process.node.chain[i + 1].block_to_json(0) == new_block.block_to_json(0)
            assert process.node.last_block.block_to_json(0) == new_block.block_to_json(0)
            assert res is True
    assert process.node.is_chain_valid()

