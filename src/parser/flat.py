import json


class Flat:
    external_id: 0
    price: 0
    link: ""
    photo: ""
    address: ""

    def __str__(self):
        return """
        Цена: ${},
        Ссылка: {}
        Фотка: {}
        Адрес: {}
        """.format(self.price, self.link, self.photo, self.address)

    def json(self):
        return json.dumps({
            "external_id": self.external_id,
            "price": self.price,
            "link": self.link,
            "photo": self.photo,
            "address": self.address,
        })