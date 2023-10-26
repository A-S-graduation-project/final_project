import csv, psycopg2
import pandas as pd
from dateutil import parser

# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()

# TABLE DATA 초기화 (테스트용) #
cur.execute("""DELETE FROM userdata""")

try:
    df = pd.read_csv("./board_info.csv")
except:
    df = pd.read_csv("./allergyProject/board_info.csv")

for line in df.values:
    board_info = [line[1],line[2],line[3],line[4],parser.parse(line[5]),'{'+line[6]+'}','{'+line[7]+'}',line[8],line[9]]

    sql = """INSERT INTO boards(bno,title,name,cno,allerinfo,cdate,ingredient,content,types,meterials)
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cur.execute(sql, board_info)
    conn.commit()

conn.close()
