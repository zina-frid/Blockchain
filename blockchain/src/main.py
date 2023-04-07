from blockchain.src.config import FIRST_PROCESS_PORT, SECOND_PROCESS_PORT, THIRD_PROCESS_PORT, SOCKET_HOST
from blockchain.src.node import Node
from flask import Flask, request
from gevent import monkey
import grequests
import threading
import logging
import time
import sys


monkey.patch_all()
logging.getLogger('werkzeug').disabled = True


class Process:

    def __init__(self, port: int):
        self.id = port % 10  # Process/Node id
        self.port = port  # Process port
        self.peer_ports = self.get_peer_ports()  # Array with peer's ports
        self.received = False  # = True, when Node received block
        self.stop = False  # = True, when stop_thread method called
        self.node = Node(self)  # Create Node instance

    def start(self):
        # Create server
        server = Flask(__name__)

        host = SOCKET_HOST
        # URLs to broadcast block
        peer_urls = [f'http://{host}:{self.peer_ports[0]}/', f'http://{host}:{self.peer_ports[1]}/']

        # Generating new block
        def generating_new_block():
            while not self.stop:
                # If chain is empty, and it is Node 1...
                if self.id == 1 and len(self.node.chain) == 0:
                    # inits genesis block
                    genesis_block = self.node.create_genesis()
                    # and broadcast it
                    self.broadcast_block(genesis_block, peer_urls)

                if len(self.node.chain) != 0:
                    # Node start generating new block
                    new_block = self.node.create_new_block()
                    # Check if generated block is not outdated
                    if not self.received:
                        self.node.chain.append(new_block)
                        self.node.last_block = new_block
                        self.broadcast_block(new_block, peer_urls)
                time.sleep(1)

        # Server POST-request handler
        @server.route("/", methods=['POST'])
        def server_handler():
            # Receive message
            received_block = request.get_json()
            self.received = True
            try:
                self.node.handle_received_block(received_block)
                time.sleep(1)
                self.received = False
                return "Received new Block"

            except BaseException as e:
                print(f"Exception: {e}")
                self.received = False
                return "Error"

        # Start threads
        server = threading.Thread(target=server.run, args=(host, self.port))
        server.setDaemon(True)
        generator = threading.Thread(target=generating_new_block)
        server.start()
        generator.start()
        time.sleep(1)

    # Broadcast message with new block
    def broadcast_block(self, block, peer_urls):
        if not self.received:
            rs = (grequests.post(u, json=block.block_to_json(self.id)) for u in peer_urls)
            grequests.map(rs)

    # Return peer ports depending on its port
    def get_peer_ports(self):
        if self.port == FIRST_PROCESS_PORT:
            return [SECOND_PROCESS_PORT, THIRD_PROCESS_PORT]
        elif self.port == SECOND_PROCESS_PORT:
            return [FIRST_PROCESS_PORT, THIRD_PROCESS_PORT]
        else:
            return [FIRST_PROCESS_PORT, SECOND_PROCESS_PORT]

    def stop_thread(self):
        self.stop = True


# Start new Process
if __name__ == '__main__':
    port_num = int(sys.argv[1])
    process = Process(port_num)
    process.start()

