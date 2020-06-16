import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS teams (name TEXT, mem1 TEXT, mem2 TEXT, mem3 TEXT, mem4 TEXT, mentor TEXT, league TEXT,\
event TEXT)"
cur.execute(query)
query = "CREATE TABLE IF NOT EXISTS refrees (login TEXT, email TEXT, password TEXT, name TEXT, secondname TEXT, league TEXT, region)"
cur.execute(query)
query = "CREATE TABLE IF NOT EXISTS Admins (Login TEXT, Password TEXT)"
cur.execute(query)
query = "INSERT INTO Admins (Login,Password) VALUES ('ADMIN', 'ADMIN')"
cur.execute(query)
conn.commit()
conn.close()