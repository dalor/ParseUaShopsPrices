from parse import *
from db import db

parsers = [silpo_parse, megamarket_parse, metro_parse, fozzy_parse, auchan_parse,
    novus_parse, varus_parse, furshet_parse, atb_parse]

def update():

    db.items.delete_many({})

    for parse in parsers:
        try:
            results = [item.to_json() for item in parse()]
            db.items.insert_many(results)
        except:
            pass

