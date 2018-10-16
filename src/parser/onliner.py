import time
from urllib.parse import urlencode

import requests

from src.storage.db import Flat
from .base_parser import BaseParser, Flats


class Onliner(BaseParser):
    url = None
    params = None
    where = "onliner"

    def __init__(self):
        self.url = "https://ak.api.onliner.by/search/apartments"
        self.params = {'rent_type[]': "1_room", 'price[max]': 250, 'currency': 'usd', 'page': 1,
                       "bounds[lb][lat]": 53.80713881129995, "bounds[lb][long]": 27.389602661132812, "bounds[rt][lat]": 53.99485396562768, "bounds[rt][long]": 27.716789245605472}

    def geturl(self):
        return self.url + "?" + urlencode(self.params)

    def set_min_price(self, price: int = None):
        return self.set_filter_by_key('price[min]', price)

    def set_max_price(self, price: int = None):
        return self.set_filter_by_key('price[max]', price)

    def set_page(self, page: int):
        return self.set_filter_by_key('page', page)

    def set_filter_by_key(self, key, val: int = None):
        if val is None:
            self.params.pop(key, None)
        else:
            self.params[key] = val

    def get_all(self, page: int = 1, flats=[]) -> Flats:
        print("try to get page {} from {}".format(page, self.where))
        self.set_page(page)

        print(self.geturl())
        r = requests.get(self.geturl())
        response = r.json()

        # todo response['errors']

        for val in response['apartments']:
            flat = Flat(
                external_id=val['id'],
                price=val['price']['converted']['USD']['amount'],
                link=val['url'],
                photo=val['photo'],
                address=val['location']['address'],
                where=self.where
            )

            flats.append(flat)

        if response['page']['current'] < response['page']['last']:
            time.sleep(1)
            return self.get_all(page+1, flats)

        return flats
