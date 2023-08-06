import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from transsnet_afnews_common.utils import IdGenerator

class TestIdGenerator(unittest.TestCase):
    def testuuid(self):
        idgen1 = IdGenerator(biz_name='test', redis_host='127.0.0.1', redis_port=6379, redis_db=0, redis_password=None)
        pool = ThreadPoolExecutor(4)
        result = {""}

        def generate_id():
            for i in range(1000000):
                result.add(idgen1.uuid('test'))

        ctrime = time.time()
        res1 = pool.submit(generate_id)
        res2 = pool.submit(generate_id)
        res3 = pool.submit(generate_id)
        res4 = pool.submit(generate_id)
        res1.result()
        res2.result()
        res3.result()
        res4.result()
        etrime = time.time()
        print(etrime - ctrime)
        print(len(result))
