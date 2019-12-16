import json

class Item:
    def __init__(self, shop, title, price, old_price, url, thumbnail, category, description):
        self.title = title
        self.price = price
        self.old_price = old_price
        self.url = url
        self.thumbnail = thumbnail
        self.category = category
        self.shop = shop
        self.description = description

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            'shop': self.shop,
            'title': self.title,
            'price': self.price,
            'old_price': self.old_price,
            'url': self.url,
            'thumbnail': self.thumbnail,
            'category': self.category,
            'description': self.description
        }