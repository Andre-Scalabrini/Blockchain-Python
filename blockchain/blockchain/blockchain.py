import hashlib
import time
import requests

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.peers = set()  # Armazena outros nós na rede

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        latest_block = self.chain[-1]
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def register_peer(self, peer_address):
        """Adiciona o endereço de outro nó."""
        self.peers.add(peer_address)

    def synchronize(self):
        """Sincroniza a cadeia com o nó mais longo na rede."""
        longest_chain = None
        max_length = len(self.chain)

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/blocks")
                if response.status_code == 200:
                    chain_data = response.json()
                    if len(chain_data) > max_length:
                        max_length = len(chain_data)
                        longest_chain = chain_data
            except requests.RequestException:
                continue

        if longest_chain:
            self.replace_chain(longest_chain)

    def replace_chain(self, chain_data):
        """Substitui a cadeia local pela nova."""
        self.chain = [Block(block['index'], block['timestamp'], block['data'], block['previous_hash'])
                      for block in chain_data]

    def to_dict(self):
        """Converte a cadeia para formato serializável."""
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            } for block in self.chain
        ]
