import json

from peewee import *

path = "main.sqlite"
db = SqliteDatabase(path)


class Flat(Model):
    id = PrimaryKeyField()
    external_id = CharField()
    price = FloatField()
    link = CharField()
    photo = CharField()
    address = CharField()
    where = CharField()

    class Meta:
        database = db

    @property
    def __str__(self):
        return """
        Цена: ${}
        Ссылка: {}
        Фотка: {}
        Адрес: {}
        """.format(self.price, self.link, self.photo, self.address)

    def __dict__(self):
        return {
            "external_id": self.external_id,
            "price": self.price,
            "link": self.link,
            "photo": self.photo,
            "address": self.address,
        }

    def json(self):
        return json.dumps(self.__dict__())


db.connect()
db.create_tables([Flat])