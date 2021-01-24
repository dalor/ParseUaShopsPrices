import json

class Item:
    def __init__(self, shop, title, price, old_price=None, url=None, thumbnail=None, category=None, description=None, unit=None, weight=None):
        self.title = title
        self.price = price
        self.old_price = old_price
        self.url = url
        self.thumbnail = thumbnail
        self.category = category
        self.shop = shop
        self.description = description
        self.unit = unit
        self.weight = weight

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
            'description': self.description,
            'unit': self.unit,
            'weight': self.weight
        }