import psycopg2


# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()



# 이후 빠진 allergy 추가 필요 #
types = ["밑반찬", "메인반찬", "국/탕", "찌개", "디저트",
         "면/만두", "밥/죽/떡", "퓨전", "김치/젓갈/장류", "양념/소스/잼",
         "양식", "샐러드", "스프", "빵", "과자",
         "차/음료/술", "기타"]

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS type_categories(
            id SERIAL PRIMARY KEY NOT NULL,
            types varchar(50) UNIQUE NOT NULL)""")

for type in types:
    # allergy를 unique field이므로 존재하는 데이터의 경우 무시 #
    try:
        sql = """INSERT INTO type_categories(id, types) VALUES(DEFAULT, '{0}')""".format(type)
        cur.execute(sql, type)
        
    except Exception as ex:
        conn.rollback() 
    else:
        conn.commit()

cur.close()
conn.close()