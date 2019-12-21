from flask import Flask, jsonify, request
from parse import *
from query import find, count
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


def prepare_query(func):
    def new():
        query_dict = {}
        for key, value in request.args.items():
            try:
                query_dict[key] = json.loads(value)
            except:
                pass
        if query_dict:
            try:
                result = func(**query_dict)
                result['ok'] = True
                return jsonify(result)
            except:
                return jsonify({'ok': False, 'error': 'Invalid query'})
        else:
            return jsonify({'ok': False, 'error': 'No query'})
    new.__name__ = func.__name__ + '_new'
    return new

@app.route('/find')
@prepare_query
def find_query(**kwargs):
    return {'items': find(**kwargs)}

@app.route('/count')
@prepare_query
def count_query(**kwargs):
    return {'count': count(**kwargs)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))