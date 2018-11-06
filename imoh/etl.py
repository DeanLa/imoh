'''DB operations'''
import sqlite3
import pandas as pd

connection = None
z = pd.DataFrame({'name': list('aaabcc'), 'number': range(6)})
# def frame_to_db(frame, connection=None)
conn = connection or sqlite3.connect('./db.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS dean
(id idx INT,
name CHAR,
number INT)
''')
z.to_sql('dean', conn, if_exists='upsert')
pd.read_sql()