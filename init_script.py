# coding=utf-8
__author__ = 'ericwu<zephor@qq.com>'

import os

import h5py
import sqlite3

from common import DATA_FILE
from common import DB_FILE
from common import TABLE


def main():
    if os.path.exists(DB_FILE):
        print "database already exists"
        return

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    print "begin to create table"
    # Create table
    c.execute("""CREATE TABLE IF NOT EXISTS %s
                 (id integer primary key autoincrement,
                  time timestamp,
                  price real,
                  quantity real,
                  side int)""" % TABLE)

    f = h5py.File(DATA_FILE, "r")
    data = f["trade"]

    print "begin to insert data..."
    c.executemany(
            "INSERT INTO %s (time, price, quantity, side) VALUES (?, ?, ?, ?)" % TABLE,
            ((int(item[0]), str(item[1]), str(item[2]), int(item[3])) for item in data))
    print "begin to build index..."
    c.execute("CREATE INDEX if not exists index_time ON %s (time)" % TABLE)
    conn.commit()
    conn.close()
    print "done"


if __name__ == "__main__":
    main()
