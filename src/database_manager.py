# -*- coding: utf-8 -*-

import pymongo
from typing import Dict

from settings import DATABASE_CONFIG


class DatabaseManager:
    _inserts_counter = 0
    # TODO: add singleton pattern to make sure to always have a single db client instance ?

    def __init__(self, host=None, port=None, db_name=None):
        self._host = host or DATABASE_CONFIG["host"]
        self._port = port or DATABASE_CONFIG["port"]
        self._db_name = db_name or DATABASE_CONFIG["db_name"]
        self._db_table_name = DATABASE_CONFIG["db_table_name"]
        # Collection is the pointer toward the mongodb "table". It's private to grant a good encapsulation
        self.__collection = None

    @property
    def inserts_count(self):
        return self._inserts_counter

    def _increment_inserts_counter(self):
        self._inserts_counter += 1

    def connect(self):
        if self.__collection is None:  # To avoid useless connections
            mongodb_client = pymongo.MongoClient(self._host, self._port)
            database = mongodb_client[self._db_name]
            self.__collection = database[self._db_table_name]
            # For optimized search, creating text-index on title and url
            self.__collection.create_index(
                [
                    ("_id", pymongo.TEXT),
                    ("title", pymongo.TEXT),
                    ("content", pymongo.TEXT),
                ]
            )

    def insert(self, element):
        self.connect()
        self.__collection.insert_one(element)
        self._increment_inserts_counter()

    def find(self, filters: Dict = None) -> pymongo.cursor.Cursor:
        self.connect()
        if filters is None:
            return self.__collection.find()
        return self.__collection.find(filters)

    def find_text(self, query: str) -> pymongo.cursor.Cursor:
        text_filter = {"$text": {"$search": query, "$caseSensitive": False}}
        return self.find(text_filter)
