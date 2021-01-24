from item import Item

import requests
import grequests


def parse_page(shop, page):
    items = []

    for item in page['results']:
        items.append(Item(shop, item['title'], item['price'] / 100, item['discount']['old_price'] /
                          100, item['web_url'], item['img']['s350x350'], item['category_id'], item['description'], item['unit'], item['weight']))

    return items


def parse(shop, path='products/promotion'):

    if not 'products' in path:
        path += '/products'

    base_url = 'https://stores-api.zakaz.ua/stores/default/' + path

    headers = {
        'x-chain': shop,
        'Accept-Language': 'uk'
    }

    response = requests.get(base_url, headers=headers).json()

    if 'errors' in response:
        return []

    items = parse_page(shop, response)

    pages = response['count'] // len(response['results']) + \
        (1 if response['count'] % len(response['results']) else 0)

    reqs = [grequests.get(
        base_url + f'?page={pnum}', headers=headers) for pnum in range(2, pages + 1)]

    for response in grequests.map(reqs):
        if response:
            items.extend(parse_page(shop, response.json()))

    return items

def make_parser(shop):

    def parser(path='products/promotion', **kwargs):
        return parse(shop, path)

    return parser
