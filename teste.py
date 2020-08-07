import sqlite3
import pandas as pd
import os
import json
import jsonify
conn = sqlite3.connect('CaseItau.sqlite3')
cursor = conn.cursor()

#
# f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases_tratadas', 'media_preco.csv')
# df = pd.read_csv(f, sep=",", encoding='utf8')
# df.to_sql('media_preco', conn, if_exists='append', index=False)

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")



cursor.execute("SELECT * FROM residencias_like ")
result = cursor.fetchall()

print(result)
