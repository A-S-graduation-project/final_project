import psycopg2


# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()



cur.execute("""CREATE TABLE IF NOT EXISTS meterial_categories(
            id SERIAL PRIMARY KEY NOT NULL,
            materials varchar(50) UNIQUE NOT NULL)""")

# 이후 빠진 allergy 추가 필요 #
meterials = ["소고기", "돼지고기", "닭고기", "육류", "채소류",
             "해물류", "달걀/유제품", "가공식품류", "쌀", "밀가루",
             "건어물류", "버섯류", "과일류", "콩/견과류", "곡류",
             "기타"]


for meterial in meterials:
    # allergy를 unique field이므로 존재하는 데이터의 경우 무시 #
    try:
        sql = """INSERT INTO meterial_categories(id, meterials) VALUES(DEFAULT, '{0}')""".format(meterial)
        print(sql)
        cur.execute(sql, meterial)
    except Exception as ex:
        conn.rollback() 
    else:
        conn.commit()

cur.close()
conn.close()