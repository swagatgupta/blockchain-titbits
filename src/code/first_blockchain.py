import datetime
import hashlib
import json


## Part 1 --> Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        new_block = self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        '''
        A block contains
            1. index of the block
            2. timestamp (exact time when block was mined)
            3. proof of block
            4. previous hash
        '''
        block = {
            'index': len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            }
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