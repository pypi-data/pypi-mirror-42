from crawler_utils import MongoCache


def test_mongo_cache():
    cache = MongoCache(username="root", password="newpass", db_name="hupu")
    length = cache.length()
    assert length == 0


def test_insert():
    pass


if __name__ == "__main__":

    test_mongo_cache()
