import sqlite3

jiting = sqlite3.connect('./db/jiting.db')
cur_jt = jiting.cursor()
cur_jt.close()

