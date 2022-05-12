import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse



## Part 2 --> Create a crypto currency transaction

class Blockchain:
    
    def __init__(self):
        '''
        Instantiate genesis block in Blockchain
        '''
        self.chain = []
        self.transactions = []
        self.node = set()
        new_block = self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        '''
        A block contains
            1. index of the block
            2. timestamp (exact time when block was mined)
            3. proof of block
            4. previous hash
            5. transactions
        '''
        block = {
            'index': len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions' : self.transactions
            }
        
        # After transactions are added to block, 
        # reinitialise it to empty as the next block will have different set of transactions
        self.transactions = []
        ## Append the block to blockchain
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        '''
        get the latest block in the blockchain
        '''
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        '''
        Create a proof of work which miner has to solve
        In this case, it is finding the proof (number) which will result in a hasvalue starting with 4 '0's
        '''
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[0:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self,block):
        '''
        Calculate the hash of the block
        '''
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        '''
        Chain if chain is valid. Following are the checks
            1. hash of previous block = previous hash of current block (ensures linking)
            2. proof of work is correct (miners have done their job)
        '''
        for i in range(1,len(chain)):
            previous_block = chain[i-1]
            current_block = chain[i]
            if self.hash(previous_block) != current_block.get('previous_hash','0000x'):
                return False
            previous_proof = previous_block.get('proof',0)
            current_proof = current_block.get('proof',0)
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[0:4] != '0000':
                return False
        return True
    
    def add_transaction(self, sender, receiver, amount):
        '''
        1. format each transaction and add them to the list of transactions for a block
        2. return the index of the block which will hold these transactions
        '''
        transaction_detail = {
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
        }
        ## Add the transaction to the transaction list
        self.transactions.append(transaction_detail)
        ## Get previous block details
        previous_block = self.get_previous_block()
        ## Return the index of the new block
        return previous_block.get('index') + 1
    
    def add_node(self, address):
        '''
        Add new node addresses to the network
        '''
        parsed_url = urlparse(address)
        self.node.add(parsed_url.netloc)
    
    def replace_chain(self):
        '''
        1. Check the length of blockchain in individual nodes
        2. Check if longest_chain exists in a different node
        3. Replace current blockchain with the longest chain from another node
        4. Return True if chain was replaces. Else return False
        '''
        network = self.node
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
            
        
