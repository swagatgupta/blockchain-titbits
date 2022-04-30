from flask import Flask, jsonify
from first_blockchain import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
    new_block = blockchain.create_block(new_proof,previous_hash)

    response = {
                "message" : "Congratulations you just mined a block",
                "block_details": new_block
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

## Run the app
app.run(host = '0.0.0.0', port = 5000)

    