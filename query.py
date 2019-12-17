from db import db

def find(query_={}):
    items = []
    for item in db.items.find(query_, show_record_id=False):
        item['_id'] = str(item['_id'])
        items.append(item)
    return items
