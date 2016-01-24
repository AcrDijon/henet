# encoding: utf8
import signal
from uuid import uuid4
from multiprocessing import Pool
from functools import partial


_pool = None
_results = {}


def store_result(res_id, res):
    _results[res_id] = res
    # XXX should log any error here


def _init_proc():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def initialize_pool():
    global _pool
    if _pool is not None:
        close_pool()
    _pool = Pool(4, _init_proc)


def close_pool():
    global _pool
    if _pool is None:
        return
    _pool.terminate()
    _pool.join()
    _pool = None


def apply_async(func, args):
    res_id = str(uuid4())
    _pool.apply_async(func, args, callback=partial(store_result, res_id))
