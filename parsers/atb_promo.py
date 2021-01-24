from item import Item

import requests

import lxml.html

import re

def parse(akcia='economy'):

    base_url = f'https://www.atbmarket.com/hot/akcii/{akcia}'

    response = requests.get(base_url).content

    page = lxml.html.fromstring(response)

    items = []

    for item in page.xpath('//ul[@class = "promo_list promo_type2"]/li'):
        title = re.sub(r'\s+', ' ', item.xpath('.//span[@class = "promo_info_text"]')[0].text_content())[1:-1]
        category = re.sub(r'\s+', ' ', item.xpath('.//span[@class = "promo_info_text"]')[0].text)[1:-1]
        thumbnail = 'https://www.atbmarket.com/' + item.xpath('.//a[@class = "promo_image_link"]/img')[0].get('src')
        url = base_url + item.xpath('.//a[@class = "promo_image_link"]')[0].get('href')
        price_block = item.xpath('.//div[@class = "promo_price"]')
        if price_block:
            price = float(price_block[0].text + '.' + price_block[0].xpath('.//span')[0].text)
        else:
            price = None
        old_price_block = item.xpath('.//span[@class = "promo_old_price"]')
        if old_price_block and old_price_block[0].text:
            old_price = float(old_price_block[0].text)
        else:
            old_price = None
        items.append(Item('atb', title, price, old_price, url, thumbnail, category, None))

    return items

