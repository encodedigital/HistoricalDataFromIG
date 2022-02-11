import sqlite3

conn = sqlite3.connect('forex.db')

def createTable(table):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS "{tablename}" (
        "id"    INTEGER,
        "snapshotTime"  TEXT NOT NULL,
        "open_ask"  REAL NOT NULL,
        "open_bid"  REAL NOT NULL,
        "close_ask" REAL NOT NULL,
        "close_bid" REAL NOT NULL,
        "high_ask"  REAL NOT NULL,
        "high_bid"  REAL NOT NULL,
        "low_ask"   REAL NOT NULL,
        "low_bid"   REAL NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    );'''.format(tablename=table))

    conn.commit()

def loadData(table, data):
    createTable(table)
    c = conn.cursor()
    c.executemany('''
        INSERT INTO {tablename} 
        (snapshotTime, open_ask, open_bid, close_ask, close_bid, 
        high_ask, high_bid, low_ask, low_bid) 
        VALUES (?,?,?,?,?,?,?,?,?);'''.format(tablename=table), data)

    conn.commit()
