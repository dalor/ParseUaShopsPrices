from item import Item

import requests

def parse(shop):

    headers = {
        'x-chain': shop,
        'Accept-Language': 'uk'
    }

    response = requests.get('https://stores-api.zakaz.ua/stores/default/products/promotion/', headers=headers).json()

    items = []

    for item in response['results']:
        items.append(Item(shop, item['title'], item['price'] / 100, item['discount']['old_price'] / 100, item['web_url'], item['img']['s350x350'], item['category_id'], item['description']))

    return items