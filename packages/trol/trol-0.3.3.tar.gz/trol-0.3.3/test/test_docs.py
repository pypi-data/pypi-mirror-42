import doctest
import unittest
import trol
from redis import Redis
from .common import ensure_redis_is_online

container_token = None
redis = None

def setUp(dtest):
    global container_token
    global redis

    container_token = ensure_redis_is_online()
    if redis is None:
        redis = Redis('localhost')
    redis.flushall()


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocFileSuite(
        'model.py', 'collection.py', 'util.py', '../README.rst', 'lock.py', package=trol, setUp=setUp))
    return tests
