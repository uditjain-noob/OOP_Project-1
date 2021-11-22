import sqlite3
from sqlite3.dbapi2 import Cursor

db = sqlite3.connect('db.sqlite3')
cur = db.cursor()

cur.execute('''
INSERT INTO Room
VALUES (1, 'deluxe');
''')

db.commit()