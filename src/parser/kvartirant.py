import time
from urllib.parse import urlencode

import requests

from src.storage.db import Flat
from .base_parser import BaseParser, Flats


class Kvartirant(BaseParser):
    url = None
    params = None
    where = "onliner"

    def __init__(self):
        self.url = "https://www.kvartirant.by/ads/flats/type/rent/"
        self.params = {
            "tx_uedbadsboard_pi1[search][q]": "",
            "tx_uedbadsboard_pi1[search][district]": 0,
            "tx_uedbadsboard_pi1[search][rooms][1]": 1,
            "tx_uedbadsboard_pi1[search][price][from]": "",
            "tx_uedbadsboard_pi1[search][price][to]": 250,
            "tx_uedbadsboard_pi1[search][currency]": 840,
            "tx_uedbadsboard_pi1[search][date]": "",
            "tx_uedbadsboard_pi1[search][agency_id]": ""
        }

    def geturl(self):
        return self.url + "?" + urlencode(self.params)

    def set_min_price(self, price: int = None):
        return self.set_filter_by_key('tx_uedbadsboard_pi1[search][price][from]', price)

    def set_max_price(self, price: int = None):
        return self.set_filter_by_key('tx_uedbadsboard_pi1[search][price][to]', price)

    def set_page(self, page: int):
        return self.set_filter_by_key('page', page)

    def set_filter_by_key(self, key, val: int = None):
        if val is None:
            self.params.pop(key, None)
        else:
            self.params[key] = val

    def get_all(self, page: int = 1, flats=[]) -> Flats:
        print("try to get page {} from {}".format(page, self.where))
        # self.set_page(page)

        print(self.geturl())
        r = requests.get(self.geturl())
        response = r.json()

        # todo response['errors']

        for val in response['apartments']:
            flat = Flat(
                where=self.where,
                created_at=val['created_at'],
                owner=val['contact']['owner'],
                external_id=val['id'],
                price=val['price']['converted']['USD']['amount'],
                link=val['url'],
                photo=val['photo'],
                address=val['location']['address'],
                latitude=val['location']['latitude'],
                longitude=val['location']['longitude']
            )

            flats.append(flat)

        if response['page']['current'] < response['page']['last']:
            time.sleep(1)
            return self.get_all(page+1, flats)

        return flats
