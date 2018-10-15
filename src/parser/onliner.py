import requests
from urllib.parse import urlencode
from src.parser.flat import Flat


class Onliner:
    url = None
    params = None

    def __init__(self):
        self.url = "https://ak.api.onliner.by/search/apartments"
        self.params = {'rent_type[]': "1_room", 'price[max]': 250, 'currency': 'usd', 'page': 1}

    def geturl(self):
        return self.url + "?" + urlencode(self.params)

    def set_min_price(self, price):
        pass

    def set_max_price(self, price):
        pass

    def get_all(self):
        flats = []

        print(self.geturl())
        r = requests.get(self.geturl())
        response = r.json()

        # todo response['errors']

        for val in response['apartments']:
            flat = Flat()
            flat.external_id = val['id']
            flat.price = val['price']['converted']['USD']['amount']
            flat.link = val['url']
            flat.photo = val['photo']
            flat.address = val['location']['address']

            flats.append(flat)

        return flats
