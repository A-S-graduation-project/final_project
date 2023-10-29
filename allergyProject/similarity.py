import psycopg2, json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def vector(category, alist, blist, clist = None):
    # count vector로 만들어서 cosine similar 만들기 #
    vectorizer = CountVectorizer()

    # alist = rawmtrl (product), allerinfo (board) #
    alist_vector = vectorizer.fit_transform(alist)
    alist_cate = cosine_similarity(alist_vector)
    
    # blist = prdkind (product), types (board) #
    blist_vector = vectorizer.fit_transform(blist)
    blist_cate = cosine_similarity(blist_vector)

    # category : 0 (product), 1 (board) #
    if category == 1:
        # blist = meterials
        clist_vector = vectorizer.fit_transform(clist)
        clist_cate = cosine_similarity(clist_vector)

        return alist_cate * 0.6 + blist_cate * 0.3 + clist_cate * 0.1
    else:
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

    food_simi_cate = vector(0, rawmtrl, prdkind)
    print(food_simi_cate)

    for x in range(row_count):
        cate_dict = {}

        for y in range(row_count):
            cate_dict[y] = food_simi_cate[x][y]

        cate_dict = sorted(cate_dict.items(), reverse=True, key=lambda x:x[1])
        source = [prdlstReportNo[x], [cate[0] for cate in cate_dict if (cate[1] >= 0.5 and cate[0] != x)]]

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
    cur.execute("""SELECT bno, allerinfo, types, meterials FROM boards""")
    brdData = cur.fetchall()
    row_count = len(brdData)
    # print(brdData[:5])

    # 전처리 #
    bno = []
    allerinfo = []
    types = []
    meterials = []

    for row in brdData:
        bno.append(row[0])
        allerinfo.append(row[1])
        types.append(row[2])
        meterials.append(row[3])

    # print(allerinfo[:5])
    # print(types[:5])
    # print(meterials[:5])

    board_simi_cate = vector(1, allerinfo, types, meterials)
    # board_simi_cate = vector(ingredient, allerinfo)
    print(board_simi_cate)

    for x in range(row_count):
        cate_dict = {}

        for y in range(row_count):
            cate_dict[y] = board_simi_cate[x][y]

        cate_dict = sorted(cate_dict.items(), reverse=True, key=lambda x:x[1])
        source = [bno[x], [cate[0] for cate in cate_dict if (cate[1] >= 0.5 and cate[0] != x)]]
    
        sql = """INSERT INTO bsimilarity(bno,simlist) VALUES(%s, %s)"""\
            """ON CONFLICT (bno) DO UPDATE SET simlist = EXCLUDED.simlist"""
        cur.execute(sql, source)
        conn.commit()

    conn.close()


# food_sim()
# board_sim()