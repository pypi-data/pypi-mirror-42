import json
from urllib.parse import quote_plus

from pymongo import mongo_client


# import configs


class MongoCache:
    def __init__(
        self,
        username,
        password,
        client=None,
        disk_cache=None,
        host="localhost",
        db_name="video_cache",
        collection_name="default",
    ):
        '''
        Cache based on Mongodb to save crawler messages

        a = MongoCache(db_name="video")
        a.items()
        a.set(key='names', value='fjl3', collection="test_cache", db_name='video')

        :param username: mongodb username
        :param password: mongodb password
        :param client:  client to connect mongodb
        :param disk_cache:  cache for disk if not exist in mongodb then will look in disk_cache
        :param host: mongodb server host
        :param db_name: database name
        :param collection_name:  collection name

        '''
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = mongo_client.MongoClient(uri) if not client else client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.disk_cache = disk_cache

    def __getitem__(self, key):
        # if db_name:
        record = self.collection.find_one({"_id": key})
        if record:
            return record["key"]
        elif self.disk_cache and self.disk_cache[key]:
            self[key] = self.disk_cache[key]
            return self.disk_cache[key]
        else:
            raise KeyError("{} cache does not exist".format(key))

    def __setitem__(self, key, value):
        self.collection.update_one({"_id": key}, {"$set": {"key": value}}, upsert=True)

    def length(self, collection=None):
        '''
        return collection all counts
        :param collection:
        :return:
        '''
        if collection:
            return self.db[collection].count()
        return self.collection.estimated_document_count()

    def items(self, collection=None):
        '''
        get all items from collection
        :param collection:
        :return: generator
        '''
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            yield r

    def keys(self, collection=None):
        '''
        get all keys from collection
        :param collection:
        :return:
        '''
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            yield r["_id"]

    def values(self, collection=None):
        '''
        get all values from collections
        :param collection:
        :return:
        '''
        if collection:
            collection = self.db[collection]
        else:
            collection = self.collection
        res = collection.find()
        for r in res:
            try:
                yield json.loads(r["key"])
            except json.JSONDecodeError:
                yield r["key"]

    def change_collection(self, collection_name):
        '''
        change collection name
        :param collection_name:
        :return:
        '''
        if not collection_name:
            return
        self.collection = self.db[collection_name]

    def set(self, collection_name, key, value):
        '''
        set key for value
        :param collection_name:
        :param key:
        :param value:
        :return:
        '''
        self.db[collection_name].update_one(
            {"_id": key}, {"$set": {"key": value}}, upsert=True
        )

    def get(self, collection_name, key):
        '''
        get value from collection by key
        :param collection_name:
        :param key:
        :return:
        '''
        record = self.db[collection_name].find_one({"_id": key})
        if not record:
            raise KeyError("{} cache does not exist".format(key))
        return record['key']

