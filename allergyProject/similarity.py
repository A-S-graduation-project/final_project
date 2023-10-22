import psycopg2, json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def vector(alist, blist):
    # count vector로 만들어서 cosine similar 만들기 #
    vectorizer = CountVectorizer()

    # alist = rawmtrl (product), ingredient (board) #
    alist_vector = vectorizer.fit_transform(alist)
    alist_cate = cosine_similarity(alist_vector)
    
    # category : 0 (product), 1 (board) #
    # blist = prdkind (product), allerinfo (board) #
    blist_vector = vectorizer.fit_transform(blist)
    blist_cate = cosine_similarity(blist_vector)

    return alist_cate * 0.3 + blist_cate * 0.7


def food_sim():
    # DB 연결 #
    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='2017018023',
                            dbname='allergydb',
                            connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "prdlstReportNo", rawmtrl, prdkind FROM products""")
    proData = cur.fetchall()
    row_count = len(proData)
    # print(proData[0:2])
    
    # 전처리 #
    prdlstReportNo = []
    rawmtrl = []
    prdkind = []

    for row in proData:
        prdlstReportNo.append(row[0])
        rawmtrl.append(row[1])
        prdkind.append(row[2])

    # print(rawmtrl[:5])
    # print(prdkind[:5])

    food_simi_cate = vector(rawmtrl, prdkind)
    print(food_simi_cate)

    for n in range(row_count):
        source = [prdlstReportNo[n], [prdlstReportNo[m] for m in range(row_count) if (food_simi_cate[n][m] >= 0.5 and prdlstReportNo[m] != prdlstReportNo[n])]]
        sql = """INSERT INTO psimilarity("prdNo",simlist) VALUES(%s, %s)"""\
            """ON CONFLICT ("prdNo") DO UPDATE SET simlist = EXCLUDED.simlist"""
        cur.execute(sql, source)
        conn.commit()

    conn.close()
    
#=========================================================================================================================================#

def board_sim():
    # DB 연결 #
    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='2017018023',
                            dbname='allergydb',
                            connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT bno, ingredient, allerinfo FROM boards""")
    brdData = cur.fetchall()
    row_count = len(brdData)
    # print(brdData[0:2])

    # 전처리 #
    bno = []
    ingredient = []
    allerinfo = []

    for row in brdData:
        bno.append(row[0])

        json_ingre = json.loads(row[1])
        ingredient.append(json_ingre['ingredient_name'])
        
        json_aller = json.loads(row[2])
        aller = ''
        for j in json_aller:
            aller += j['allergy'] + ' '
        allerinfo.append(''.join(aller.rstrip()))

    # print(ingredient)
    # print(allerinfo)

    board_simi_cate = vector(allerinfo, ingredient)
    # board_simi_cate = vector(ingredient, allerinfo)
    print(board_simi_cate)

    for n in range(row_count):
        source = [bno[n], [bno[m] for m in range(row_count) if (board_simi_cate[n][m] >= 0.5 and bno[m] != bno[n])]]
        sql = """INSERT INTO bsimilarity(bno,simlist) VALUES(%s, %s)"""\
            """ON CONFLICT (bno) DO UPDATE SET simlist = EXCLUDED.simlist"""
        cur.execute(sql, source)
        conn.commit()

    conn.close()


# food_sim()
# board_sim()