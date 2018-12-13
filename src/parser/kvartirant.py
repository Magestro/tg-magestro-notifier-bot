import re
from urllib.parse import urlencode

import requests
from pyquery import PyQuery

from src.storage.db import Flat
from .base_parser import BaseParser, Flats


class Kvartirant(BaseParser):
    url = None
    params = None
    where = "kvartirant"

    def __init__(self):
        self.url = "https://www.kvartirant.by/ads/flats/type/rent/"
        self.params = {
            "tx_uedbadsboard_pi1[search][q]": "",
            "tx_uedbadsboard_pi1[search][district]": 0,
            "tx_uedbadsboard_pi1[search][rooms][1]": 1,
            "tx_uedbadsboard_pi1[search][price][from]": "",
            "tx_uedbadsboard_pi1[search][price][to]": 300,
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

    def set_filter_by_key(self, key, val: int = None):
        if val is None:
            self.params.pop(key, None)
        else:
            self.params[key] = val

    def get_all(self, page: int = 1, flats=[]) -> Flats:
        print("try to get page {} from {}".format(page, self.where))

        print(self.geturl())
        r = requests.get(self.geturl())
        pq = PyQuery(r.content.decode())
        items = pq('table.ads_list_table tr')

        for val in items.items():
            if val.find('.title a').attr('href') is None:
                continue

            ext_id = int(val.find('.title a').attr('href').split("/")[-2])
            if ext_id <= 0:
                continue

            if val.find('.img') is not None:
                photo = "https://www.kvartirant.by" + val.find('img').attr('src')
            else:
                photo = ""

            flat = Flat(
                where=self.where,
                created_at=val.find('.date').text(),
                owner=val.find('.owner').text() == "собственник",
                external_id=str(ext_id),
                price=re.sub('[^0-9]', '', val.find('.price-box').text()),
                link=val.find('.title a').attr('href'),
                photo=photo,
                address=val.find('.rooms').text()
            )

            flats.append(flat)

        return flats
