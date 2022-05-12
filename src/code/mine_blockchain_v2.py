from uuid import uuid4
from flask import Flask, jsonify, request
from first_transaction import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

## Creating an address for the node on port 5000
node_address = str(uuid4()).replace("-","")

## Get blockchain object
blockchain = Blockchain()

## Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    '''
    Mine a new block
    '''
    previous_block = blockchain.get_previous_block()
    print (previous_block)
    previous_proof = previous_block['proof']
    new_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Swagata', amount = 1)
    new_block = blockchain.create_block(new_proof,previous_hash)

    response = {
                "message" : "Congratulations you just mined a block",
                "block_details": new_block,
                "transactions" : new_block['transactions']
                }
    return jsonify(response), 200


@app.route('/get_chain', methods = ['GET'])
def get_chain():
    '''
    Get the whole blockchain
    '''
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    '''
    Get the validity of the blockchain
    '''
    response = {
        'is_valid' : blockchain.is_chain_valid(blockchain.chain),
    }
    return jsonify(response), 200

## Adding transactions to blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    '''
    Add transactions for the new block
    '''
    json = request.get_json()
    transaction_keys  = ['sender', 'receiver','amount']
    
    if not (set(transaction_keys).issubset(set(json.keys()))):
        return 'Some elements of the transaction are missing', 400
    
    index = blockchain.add_transaction(sender = json['sender'], receiver = json['receiver'], amount = json['amount'])
    response = {'message' : f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

## Adding new nodes to the network
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    '''
    Add nodes to the blockchain
    '''
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node addresses provided', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'New nodes are connected. Following are the nodes',
        'nodes' : list(blockchain.node)
        }
    return jsonify(response), 201



@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    '''
    Replace bloclchain with the longest chain
    '''
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
        'message': 'Blockchain replaced by longest chain',
        'new_chain' : blockchain.chain
    }
    else:
        response = {
            'message': 'Blockchain is valid. No replacement necessary',
            'original_chain' : blockchain.chain
    }
    return jsonify(response), 200

## Run the app
app.run(host = '0.0.0.0', port = 5000)

    