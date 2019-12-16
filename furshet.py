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

    for item in page.xpath('//div[@class = "actions-list__action swiper-slide"]'):
        title = item.xpath('.//div[@class = "desc"]/p')[0].text
        price_block = item.xpath('.//div[@class = "cost"]')
        if price_block:
            price = float(price_block[0].text + '.' + price_block[0].xpath('.//sup')[0].text)
        else:
            price = None
        old_price_block = item.xpath('.//div[@class = "del-cost"]')
        if old_price_block:
            old_price = float(old_price_block[0].text + '.' + old_price_block[0].xpath('.//sup')[0].text)
        else:
            old_price = None
        thumbnail = item.xpath('.//div[@class = "img"]/img')[0].get('data-pagespeed-lazy-src')
        items.append(Item('furshet', title, price, old_price, None, thumbnail, None, None))

    return items

def parse():

    base_url = 'https://furshet.ua/actions'

    page = lxml.html.fromstring(requests.get(base_url, headers=headers).content)

    last_page = int(page.xpath('//li[@class = "pager-last last"]/a')[0].get('href').split('page=')[1])

    items = parse_page(page)

    reqs = [grequests.get(base_url + f'?page={pnum}', headers=headers) for pnum in range(1, last_page + 1)]

    for response in grequests.map(reqs):
        if response:
            items.extend(parse_page(lxml.html.fromstring(response.content)))

    return items