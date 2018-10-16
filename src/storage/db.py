from peewee import *

from src.storage.flat import Flat


class DB:
    path = "main.sqlite"
    db = None

    def get_db(self) -> SqliteDatabase:
        if self.db is None:
            self.db = SqliteDatabase(self.path)
            self.db.connect()
            self.db.create_tables([Flat])

        return self.db
