from flask import Flask, jsonify
from parse import *

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

@app.route('/shops')
def shops_list():
    return jsonify({'ok': True, 'shops': list(shops.keys())})

@app.route('/shop/<shop>')
def parse_shop(shop):
    shop_parse = shops.get(shop)
    if not shop_parse:
        return jsonify({'ok': False, 'error': 'No such shop'})
    # try:
    return jsonify({'ok': True, 'items': [item.to_json() for item in shop_parse()]})
    # except:
    #     return jsonify({'ok': False, 'error': 'Parse error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))