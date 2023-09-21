import psycopg2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# DB 연결 #
conn = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='2017018023',
                        dbname='allergydb',
                        connect_timeout=32768)
cur = conn.cursor()

# Mysql에서 DATA 읽기 (전처리 포함) #
cur.execute("""SELECT "prdlstReportNo", rawmtrl FROM products""")
proData = cur.fetchall()
row_count = len(proData)
# print(proData[0:2])                                             # product data 확인용                                          # user data 확인용

# 전처리 #
prdlstReportNo = []
rawmtrl = []

for row in proData:
    prdlstReportNo.append(row[0])
    rawmtrl.append(row[1])

# count vector로 만들어서 cosine similar 만들기 #
vectorizer = CountVectorizer()
food_vector = vectorizer.fit_transform(rawmtrl)
food_simi_cate = cosine_similarity(food_vector, food_vector)

print(food_simi_cate)

for n in range(row_count):
    source = [prdlstReportNo[n], [prdlstReportNo[m] for m in range(row_count) if (food_simi_cate[n][m] >= 0.5 and prdlstReportNo[m] != prdlstReportNo[n])]]
    sql = """INSERT INTO similarity("prdNo",simlist) VALUES(%s, %s)"""\
        """ON CONFLICT ("prdNo") DO UPDATE SET simlist = EXCLUDED.simlist"""
    cur.execute(sql, source)
    conn.commit()

print("\n")

conn.close()