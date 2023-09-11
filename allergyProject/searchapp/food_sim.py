import pymysql
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# DB 연결 #
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='2017018023',
                       db='allergydb',
                       charset='utf8')
cur = conn.cursor()

# Mysql에서 DATA 읽기 (전처리 포함) #
cur.execute("""SELECT prdlstReportNo, rawmtrl FROM products""")
proData = cur.fetchall()
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
print("\n")

conn.close()