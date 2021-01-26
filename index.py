from flask import Flask, jsonify, request
from shop_parse import *
from parsers.zakaz.parser import make_parser
# from query import find, count
from flask_cors import CORS
import json

import os

app = Flask(__name__)
CORS(app)

shops = {
    'auchan': {'parser': auchan_parse, 'title': 'Ашан'},
    'citymarket': {'parser': citymarket_parse, 'title': 'Сітімаркет'},
    'ekomarket': {'parser': ekomarket_parse, 'title': 'Екомаркет'},
    'furshet': {'parser': furshet_parse, 'title': 'Фуршет'},
    'megamarket': {'parser': megamarket_parse, 'title': 'Мегамаркет'},
    'metro': {'parser': metro_parse, 'title': 'Метро'},
    'novus': {'parser': novus_parse, 'title': 'Новус'},
    'varus': {'parser': varus_parse, 'title': 'Варус'}
}


@app.route('/shops')
def shops_list():
    return jsonify({'ok': True, 'shops': [
        {
            'name': shop_name,
            'title': shop['title']
        }
        for shop_name, shop in shops.items()]})

def send_parsed(parser):
    try:
        return jsonify({'ok': True, 'items': [item.to_json() for item in parser(**dict(request.args))]})
    except:
        return jsonify({'ok': False, 'error': 'Parse error'})

@app.route('/shop/<shop>')
def parse_shop(shop):
    shop_parse = shops.get(shop)
    if not shop_parse:
        return jsonify({'ok': False, 'error': 'No such shop'})
    return send_parsed(shop_parse['parser'])


@app.route('/shop/zakaz_all')
def parse_shop_zakaz_all():
    return send_parsed(zakaz_all_parse)

@app.route('/shop/zakaz_all/<shops>')
def parse_shop_zakaz_all_shops(shops):
    return send_parsed(make_parser(shops.split(',')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
