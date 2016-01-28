# encoding: utf8
import signal
import traceback
from uuid import uuid4
from multiprocessing import Pool
from functools import partial
from collections import defaultdict
import time

from henet import logger


def _run(func, *args):
    try:
        result = func(*args)
    except Exception:
        return False, traceback.format_exc()
    return True, result


class MemoryWorkers(object):
    def __init__(self, size=4):
        self.size = 4
        self._results = {}
        self._in_progress = defaultdict(list)
        self._pool = Pool(self.size, self._init_proc)

    def get_result(self, res_id):
        return self._results[res_id]

    def _store_result(self, name, res_id, res):
        logger.debug('Got result back for %s' % res_id)
        self._in_progress[name].remove(res_id)
        success, result = res
        self._results[res_id] = res
        if not success:
            logger.error(result)

    def _init_proc(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def in_progress(self, name):
        return self._in_progress[name]

    def close(self):
        self._pool.terminate()
        self._pool.join()

    def apply_async(self, name, func, args=None):
        if args is None:
            args = tuple()
        res_id = str(uuid4())
        self._in_progress[name].append(res_id)
        logger.debug('Running %s async - id: %s' % (func, res_id))
        callback = partial(self._store_result, name, res_id)
        cmd = partial(_run, func)
        res = self._pool.apply_async(cmd, args, callback=callback)
        time.sleep(.1)
        if res.ready() and not res.successful():
            try:
                res.get()
            except Exception, e:
                callback((False, str(e)))
        return res_id
