from db import db

def find(**kwargs):
    items = []
    for item in db.items.find(**kwargs):
        item['_id'] = str(item['_id'])
        items.append(item)
    return items

def count(**kwargs):
    return db.items.count(**kwargs)
