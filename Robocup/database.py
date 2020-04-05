import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS teams (name TEXT, mem1 TEXT, mem2 TEXT, mem3 TEXT, mem4 TEXT, mentor TEXT, league TEXT)"
cur.execute(query)

        