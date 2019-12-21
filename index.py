from flask import Flask, jsonify, request
from parse import *
from query import find
import json

import os

app = Flask(__name__)

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

def add_cross_origin(func):
    def new(*args, **kwargs):
        resp = func(*args, **kwargs)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp
    new.__name__ = func.__name__ + '_new'
    return new

@app.route('/shops')
@add_cross_origin
def shops_list():
    return jsonify({'ok': True, 'shops': list(shops.keys())})

@app.route('/shop/<shop>')
@add_cross_origin
def parse_shop(shop):
    shop_parse = shops.get(shop)
    if not shop_parse:
        return jsonify({'ok': False, 'error': 'No such shop'})
    try:
        return jsonify({'ok': True, 'items': [item.to_json() for item in shop_parse()]})
    except:
        return jsonify({'ok': False, 'error': 'Parse error'})

@app.route('/find')
@add_cross_origin
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