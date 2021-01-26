from item import Item
import asyncio
import aiohttp


def parse_page(shop, page):
    items = []

    for item in page['results']:
        items.append(Item(shop, item['title'], item['price'] / 100, item['discount']['old_price'] /
                          100, item['web_url'], item['img']['s350x350'], item['category_id'], item['description'], item['unit'], item['weight']))

    return items


async def prepare_requests(session, shop, path, search, page, category, all):

    params = {}

    if all:
        page = None

    if search:
        path = 'products/search'
        params['q'] = search

    if category:
        path = 'categories/{}/products'.format(category)

    base_url = 'https://stores-api.zakaz.ua/stores/default/' + path

    headers = {
        'x-chain': shop,
        'Accept-Language': 'uk'
    }

    if page:
        params['page'] = page

    async def get(page=None):
        paramss = params.copy()
        if page:
            paramss['page'] = page
        async with session.get(base_url, headers=headers, params=paramss) as resp:
            json_ = await resp.json()
            if not 'errors' in json_:
                return json_

    response = await get()

    if not response:
        return []

    items = parse_page(shop, response)

    if all:

        try:

            pages = response['count'] // len(response['results']) + \
                (1 if response['count'] % len(response['results']) else 0)

        except ZeroDivisionError:

            pages = 0

        resps = await asyncio.gather(*[get(page=pnum) for pnum in range(2, pages + 1)])

        for resp in resps:
            if resp:
                items.extend(parse_page(shop, resp))

    return items


def parse(shops, path='products/promotion', search=None, page=None, category=None, all=False, **kwargs):

    async def load_all():

        items = []

        async with aiohttp.ClientSession() as session:

            for items_ in await asyncio.gather(*[prepare_requests(session, shop, path, search, page, category, all) for shop in shops]):
                items.extend(items_)

        return items

    loop = asyncio.new_event_loop()
    return loop.run_until_complete(load_all())


def make_parser(shop):

    if not type(shop) is list:
        shop = [shop]

    def parser(**kwargs):
        return parse(shop, **kwargs)

    return parser
