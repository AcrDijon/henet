# encoding: utf8
import unittest
import time

from henet.workers import MemoryWorkers


def boom():
    raise Exception('ok')


class TestMemoryWorkers(unittest.TestCase):
    def setUp(self):
        self.workers = MemoryWorkers(size=1)

    def tearDown(self):
        self.workers.close()

    def test_async(self):
        workers = self.workers
        workers.apply_async('some-sleep', time.sleep, (1,))
        pids = workers.in_progress('some-sleep')
        self.assertEqual(len(pids), 1)
        time.sleep(1.1)
        self.assertEqual(workers.in_progress('some-sleep'), [])

    def test_async_fails(self):
        workers = self.workers
        res_id = workers.apply_async('exc', boom)
        time.sleep(.2)
        res = workers.get_result(res_id)
        self.assertFalse(res[0])
        self.assertTrue('Traceback' in res[1])

    def test_async_fails_bad_func(self):
        workers = self.workers

        def this_thing_cant_get_pickled():
            pass

        res_id = workers.apply_async('exc', this_thing_cant_get_pickled)
        time.sleep(.2)
        res = workers.get_result(res_id)
        self.assertFalse(res[0])
        self.assertTrue("Can't pickle" in res[1])
