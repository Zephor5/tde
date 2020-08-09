# coding=utf-8

__author__ = "ericwu<zephor@qq.com>"

import logging
import sqlite3
import time
from cStringIO import StringIO

import tornado.ioloop
import tornado.web
import tornado.httpserver
# import json
import ujson as json


from cachetools import LRUCache, cachedmethod
from common import DB_FILE
from common import TABLE


logger = logging.getLogger(__file__)


class TreeQueryHandler(tornado.web.RequestHandler):
    data_tree = None

    @classmethod
    def init(cls):
        if cls.data_tree:
            logger.info("data tree already initialized")
            return
        import h5py
        from common import DATA_FILE
        from tree import AVLTree

        f = h5py.File(DATA_FILE, "r")
        data = f["trade"]
        tree = cls.data_tree = AVLTree()
        import time
        st = time.time()
        logger.info("begin to init avl tree at %s", st)
        for item in data:
            t = int(item[0])
            tree.insert(t, [t, float(item[1]), float(item[2]), int(item[3])])
        logger.info("init finished taken %s", time.time() - st)

    def get(self, start_time, end_time):
        res = self.data_tree.search(int(start_time), int(end_time))
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(
                {"msg": None, "code": 0, "data": {"total": len(res), "items": res}}))


RES_CACHE = None


class DBQueryHandler(tornado.web.RequestHandler):
    CONN = None

    @classmethod
    def init(cls):
        global RES_CACHE
        if cls.CONN is None:
            cls.CONN = sqlite3.connect(DB_FILE)
            # conn = sqlite3.connect(DB_FILE)
            # tempfile = StringIO()
            # for line in conn.iterdump():
            #     tempfile.write('%s\n' % line)
            # conn.close()
            # tempfile.seek(0)
            #
            # # Create a database in memory and import from tempfile
            # cls.CONN = sqlite3.connect(":memory:")
            # cls.CONN.cursor().executescript(tempfile.read())
            # cls.CONN.commit()
            # del tempfile
        if RES_CACHE is None:
            RES_CACHE = LRUCache(1000)
        print "init finished"

    def get_data(self, start_time, end_time):
        res = {"msg": None, "code": 0, "data": None}
        try:
            cur = self.CONN.cursor()
            cur.execute("select * from %s where time >= %s and time <= %s" % (
                TABLE, start_time, end_time))
            data = cur.fetchall()
            res["data"] = {"total": len(data), "items": data}
        except Exception as e:
            logger.error("error in fetching data: %s", str(e), exc_info=True)
            res["code"] = 1  # TODO: error code
            res["msg"] = str(e)
        return res

    # @cachedmethod(lambda _: RES_CACHE)
    # @tornado.gen.coroutine
    def get(self, start_time, end_time):
        # executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        # res = yield executor.submit(self.get_data, start_time, end_time)
        res = self.get_data(start_time, end_time)
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(res))


class ApiStatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish("ok: %s" % time.time())


application = tornado.web.Application([
    (r"/api/status", ApiStatusHandler),
    (r"/api/trade/xrpusdt/(?P<start_time>\d{13})...(?P<end_time>\d{13})",
     DBQueryHandler),
])


def main():
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    # TreeQueryHandler.init()  tested slower than dbquery
    DBQueryHandler.init()  # init db after process forked
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
