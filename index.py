from flask import Flask, jsonify, request
from parse import *
from query import find
from flask_cors import CORS
import json

import os

app = Flask(__name__)
CORS(app)

shops = {
    'atb': atb_parse,
    'auchan': auchan_parse,
    'fozzy': fozzy_parse,
    'furshet': furshet_parse,
    'megamarket': megamarket_parse,
    'metro': metro_parse,
    'novus': novus_parse,
    'silpo': silpo_parse,
    'varus': varus_parse
}

@app.route('/shops')
def shops_list():
    return jsonify({'ok': True, 'shops': list(shops.keys())})

@app.route('/shop/<shop>')
def parse_shop(shop):
    shop_parse = shops.get(shop)
    if not shop_parse:
        return jsonify({'ok': False, 'error': 'No such shop'})
    try:
        return jsonify({'ok': True, 'items': [item.to_json() for item in shop_parse()]})
    except:
        return jsonify({'ok': False, 'error': 'Parse error'})

@app.route('/find')
def find_query():
    query_dict = {}
    for key, value in request.args.items():
        try:
            query_dict[key] = json.loads(value)
        except:
            pass
    if query_dict:
        try:
            return jsonify({'ok': True, 'items': find(**query_dict)})
        except:
            return jsonify({'ok': False, 'error': 'Invalid query'})
    else:
        return jsonify({'ok': False, 'error': 'No query'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))