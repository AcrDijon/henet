# encoding: utf8
import signal
import traceback
from uuid import uuid4
from multiprocessing import Pool
from functools import partial

from henet import logger


_pool = None
_results = {}


def store_result(res_id, res):
    logger.debug('Got result back for %s' % res_id)
    success, result = res
    _results[res_id] = res
    if not success:
        logger.error(result)


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


def _run(func, *args):
    try:
        result = func(*args)
    except Exception:
        return False, traceback.format_exc()
    return True, result


def apply_async(func, args):
    res_id = str(uuid4())
    logger.debug('Running %s async - id: %s' % (func, res_id))
    _pool.apply_async(partial(_run, func),
                      args, callback=partial(store_result, res_id))
