# coding=utf-8

__author__ = "ericwu<zephor@qq.com>"

import sqlite3
import unittest

import h5py

import init_script
from common import DATA_FILE, DB_FILE, TABLE


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_script.main()
        f = cls.hf = h5py.File(DATA_FILE, "r")
        cls.data_length = f["trade"].shape[0]
        cls.db = sqlite3.connect(DB_FILE)

    @classmethod
    def tearDownClass(cls):
        cls.hf.close()
        cls.db.close()

    def test_db(self):
        cur = self.db.cursor()
        cur.execute("select count(*) from %s" % TABLE)
        n = cur.fetchone()[0]
        self.assertEqual(n, self.data_length)


if __name__ == "__main__":
    unittest.main()
