from flask import Flask, send_from_directory
from flask import jsonify
from flask import request
from flask import render_template
import json
import blockchain
import os
import blockchain
import core
import logging

app = Flask(__name__,template_folder='./templates')

cache ={}
def get_blockchain():
    cached_blockchain = cache.get('blockchain')
    if not cached_blockchain:
        mw = blockchain.Wallet()
        cache['blockchain'] = blockchain.BlockChain(
            blockchain_address=mw.blockchain_address,
            port = app.config['port']
        )
        app.logger.warning({
            'private_key':mw.private_key,
            'public_key':mw.public_key,
            'blockchain_address':mw.blockchain_address
        })
    return cache['blockchain']


@app.route('/')
def index():
    return render_template('./main.html')


@app.route('/chain',methods =['GET'])
def get_chain():
    block_chain = get_blockchain()
    response = {
        'chain': block_chain.chain
    }
    return jsonify(response),200


@app.route('/transactions',methods = ["GET","POST"])
def transaction():
    block_chain = get_blockchain()
    if request.method == 'GET':
        transactions = block_chain.transaction_pool
        response ={
            'transactions':transactions,
            'length':len(transactions)
        }
        return jsonify(response),200

    if request.method == 'POST':
        request_json = request.json
        required = (
            'sender_address',
            'recipient_address',
            'value',
            'my_number',
            'place',
            'sender_public_key',
            'signature',
        )
        if not all(k in request_json for k in required):
            return jsonify({'message':'missing values'}),400
        is_created =block_chain.create_transaction(
            request_json['sender_address'],
            request_json['recipient_address'],
            request_json['value'],
            request_json['my_number'],
            request_json['place'],
            request_json['sender_public_key'],
            request_json['signature'],
        )
        if not is_created:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success'}), 201

@app.route('/mining', methods=['GET'])
def mine():
    block_chain = get_blockchain()
    is_mined = block_chain.mining()
    if is_mined:
        return jsonify({'message': 'success'}), 200
    return jsonify({'message': 'fail'}), 400

"""
@app.route('/search',methods = ['POST'])
def search():
    if request.method == 'POST':
        request_json = request.json
        required = (
            'sender_address',
            'recipient_address',
            'value',
            'my_number',
            'place',
            'sender_public_key',
            'signature',
        )
"""

@app.route('/amount', methods=['GET'])
def total_amount():
    blockchain_address= request.args['blockchain_address']
    return jsonify({
        'amount': get_blockchain().total(blockchain_address)
    }), 200




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




if __name__ == "__main__":
    from argparse import ArgumentParser
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-p','--port',default=5000,type=int,help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.config['port'] = port

    app.run(host='0.0.0.0',port=port,threaded=True,debug=True)
