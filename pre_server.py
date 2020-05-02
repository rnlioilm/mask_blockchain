from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests
import urllib.parse


import blockchain

app = Flask(__name__,template_folder='./templates')

@app.route('/')
def index():
    return render_template('./pre.html')

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

@app.route('/prefecture',methods = ["POST"])
def create_wallet():
    my_wallet = blockchain.Wallet()
    #私有鍵と公開鍵は一応です。セキュリティに問題があれば省いてください。
    response = {
        'private_key':my_wallet.private_key,
        'public_key':my_wallet.public_key,
        'blockchain_address':my_wallet.blockchain_address
    }
    return jsonify(response),200

@app.route('/amount', methods=['GET'])
def get_total_amount():
    blockchain_address= request.args['blockchain_address']
    return jsonify({
        'amount': get_blockchain().total(blockchain_address)
    }), 200





@app.route('/wallet/amount', methods=['GET'])
def calculate_amount():
    required = ['blockchain_address']
    if not all(k in request.args for k in required):
        return 'Missing values', 400

    my_blockchain_address = request.args.get('blockchain_address')
    response = requests.get(
        urllib.parse.urljoin(app.config['gw'], 'amount'),
        {'blockchain_address': my_blockchain_address},
        timeout=4)
    if response.status_code == 200:
        total = response.json()['amount']
        return jsonify({'message': 'success', 'amount': total}), 200
    return jsonify({'message': 'fail', 'error': response.content}), 400

@app.route('/maps')
def maps():
    return render_template('./map.html')

@app.route('/maps/amount', methods=['GET'])
def map():
    required = ['blockchain_address']
    #if not all(k in request.args for k in required):
    #    return 'Missing values', 400

    my_blockchain_address = request.args.get('blockchain_address')
    response = requests.get(
        urllib.parse.urljoin(app.config['gw'], 'amount'),
        {'blockchain_address': my_blockchain_address},
        timeout=4)
    if response.status_code == 200:
        total = response.json()['amount']
        return jsonify({'message': 'success', 'amount': total}), 200
    return jsonify({'message': 'fail', 'error': response.content}), 400


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9090, type=int, help='port to listen on')
    parser.add_argument('-g', '--gw', default="http://127.0.0.1:5000", type=str, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.config['gw'] = args.gw

    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)