from blockchain.src.main import Process
import time
import pytest


# check all three chains on different length
def test_nodes_and_blockchains():
    length = [5, 10, 15]

    process3 = Process(8003)
    process2 = Process(8002)
    process1 = Process(8001)

    process3.start()
    process2.start()
    process1.start()

    # check genesis
    while len(process3.node.chain) < 2 or len(process2.node.chain) < 2:
        time.sleep(1)

    assert process3.node.chain[0].block_to_json(1) == process2.node.chain[0].block_to_json(1)
    assert process2.node.chain[0].block_to_json(1) == process1.node.chain[0].block_to_json(1)
    assert process3.node.chain[0].block_to_json(1) == process1.node.chain[0].block_to_json(1)

    while len(process3.node.chain) < length[0] + 2 or len(process2.node.chain) < length[0] + 2 or len(
            process1.node.chain) < length[0] + 2:
        time.sleep(1)

    chain1_0 = process1.node.chain_to_string(length[0])
    chain2_0 = process2.node.chain_to_string(length[0])
    chain3_0 = process3.node.chain_to_string(length[0])

    assert chain1_0 == chain2_0 == chain3_0
    assert process1.node.is_chain_valid() and process2.node.is_chain_valid() and process3.node.is_chain_valid()

    while len(process3.node.chain) < length[1] + 2 or len(process2.node.chain) < length[1] + 2 or len(
            process1.node.chain) < length[1] + 2:
        time.sleep(1)

    chain1_1 = process1.node.chain_to_string(length[1])
    chain2_1 = process2.node.chain_to_string(length[1])
    chain3_1 = process3.node.chain_to_string(length[1])

    assert chain1_1 == chain2_1 == chain3_1
    assert process1.node.is_chain_valid() and process2.node.is_chain_valid() and process3.node.is_chain_valid()

    while len(process3.node.chain) < length[2] + 2 or len(process2.node.chain) < length[2] + 2 or len(
            process1.node.chain) < length[2] + 2:
        time.sleep(1)

    chain1_2 = process1.node.chain_to_string(length[2])
    chain2_2 = process2.node.chain_to_string(length[2])
    chain3_2 = process3.node.chain_to_string(length[2])

    assert chain1_2 == chain2_2 == chain3_2
    assert process1.node.is_chain_valid() and process2.node.is_chain_valid() and process3.node.is_chain_valid()

    process3.stop_thread()
    process2.stop_thread()
    process1.stop_thread()
