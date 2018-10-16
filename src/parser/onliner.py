from urllib.parse import urlencode

import requests

from src.parser.base_parser import BaseParser, Flats
from src.storage.flat import Flat


class Onliner(BaseParser):
    url = None
    params = None
    where = "onliner"

    def __init__(self):
        self.url = "https://ak.api.onliner.by/search/apartments"
        self.params = {'rent_type[]': "1_room", 'price[max]': 250, 'currency': 'usd', 'page': 1}

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

    def get_all(self) -> Flats:
        flats = []

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

        return flats
