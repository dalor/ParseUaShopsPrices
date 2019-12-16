from item import Item

import requests
import grequests

from gevent import monkey
monkey.patch_all()

import lxml.html

import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

def parse_page(page):

    items = []

    base_url = 'https://varus.ua/node/'

    for item in page.xpath('//li[@class = "action_item                "]'):
        title = re.sub(r'\s+', ' ', item.xpath('.//div[@class = "description"]')[0].text_content())[1:-1]
        category = item.xpath('.//div[@class = "description"]/h4')[0].text
        price_block = item.xpath('.//span[@class = "new"]')
        if price_block:
            price = float(price_block[0].text + '.' + price_block[0].xpath('.//span')[0].text)
        else:
            price = None
        old_price_block = item.xpath('.//span[@class = "old"]')
        if old_price_block:
            old_price = float(old_price_block[0].text + '.' + old_price_block[0].xpath('.//span')[0].text)
        else:
            old_price = None
        thumbnail = item.xpath('.//div[@class = "img"]/img')[0].get('src')
        items.append(Item('varus', title, price, old_price, base_url + item.get('id'), thumbnail, category, None))

    return items

def parse():

    base_url = 'https://varus.ua/uk/actions_list'

    page = lxml.html.fromstring(requests.get(base_url, headers=headers).content)

    last_page = int(page.xpath('//li[@class = "pager-last last"]/a')[0].get('href').split('page=')[1])

    items = parse_page(page)

    reqs = [grequests.get(base_url + f'?page={pnum}', headers=headers) for pnum in range(1, last_page + 1)]

    for response in grequests.map(reqs):
        if response:
            items.extend(parse_page(lxml.html.fromstring(response.content)))

    return items

    