import psycopg2


# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS allergies(
            ano SERIAL PRIMARY KEY NOT NULL,
            allergy varchar(45) UNIQUE NOT NULL)""")

# 이후 빠진 allergy 추가 필요 #
allergies = {'메밀', '밀', '콩', '대두', '땅콩',
               '호두', '잣', '아몬드', '소고기(쇠고기)', '닭고기',
               '돼지고기', '생선', '오징어', '갑각류', '게',
               '새우', '복숭아', '토마토', '달걀', '우유',
               '조개류', '굴', '전복', '홍합', '아황산류',
               '토마토', '무', '메추리알'}

for allergy in allergies:
    sql = """INSERT INTO allergies(allergy) VALUES (%s)"""

    # allergy를 unique field이므로 존재하는 데이터의 경우 무시 #
    try:
        cur.execute(sql, allergy)
        conn.commit()
    except:
        continue

conn.close()