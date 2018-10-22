import json
import os

from peewee import *
path = os.path.realpath(os.getcwd() + "/volume/main.sqlite")  # todo
db = SqliteDatabase(path)


class Flat(Model):
    id = PrimaryKeyField()
    where = CharField()
    external_id = CharField()

    created_at = DateTimeField()
    owner = BooleanField()
    price = FloatField()
    link = CharField()
    photo = CharField()
    address = CharField()

    latitude = CharField()
    longitude = CharField()

    class Meta:
        database = db

    def json(self):
        return json.dumps(self.__dict__)


db.connect()
db.create_tables([Flat])