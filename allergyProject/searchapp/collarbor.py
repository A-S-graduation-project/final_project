import pymysql, psycopg2
import pandas as pd
import numpy as np


def user_based_recommendation(user, user_similarity, user_item_matrix, cnoData):
    # Get the index of the active user
    user_index = list(user_item_matrix.index).index(user)
    # Find similar users and their similarity scores
    similar_users = list(enumerate(user_similarity[user_index]))
    # Sort the similar users by similarity score in descending order
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    # Initialize recommendations dictionary
    recommendations = {}

    # Iterate through similar users and their interactions
    for user_id, similarity_score in similar_users:
        if user_id == user_index:
            continue  # Skip the active user
        for item in user_item_matrix.columns:
            if user_item_matrix.at[user, item] == 0 and user_item_matrix.at[cnoData[user_id][1], item] > 0:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += similarity_score * user_item_matrix.at[cnoData[user_id][1], item]
    
    # Sort the recommendations by score in descending order
    recommendations = dict(sorted(recommendations.items(), key=lambda x: x[1], reverse=True))
    
    return recommendations


def food_recommend(user):
    conn = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='2017018023',
                        dbname='allergydb',
                        connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT cno, username, allerinfo FROM customers""")
    cnoData = cur.fetchall()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "prdlstReportNo" FROM products""")
    proData = cur.fetchall()
    # print(proData[0:2])

    cur.execute("""SELECT "CNO_id", "FNO_id" FROM fbookmark""")
    fbData = cur.fetchall()
    # print(choData[0:2])

    # print(cnoData[0:2])
    # 알레르기를 통한 사용자 유사도 #
    user_all_similarity = user_allergy_similarity()

    # rating 데이터 만들기 #
    data = {'User':[cno[1] for cno in cnoData]}

    for pro in proData:
        data[pro[0]] = [0 for _ in cnoData]

    # bookmark data 적용 #
    for fbno in fbData:
        if fbno[0] != None:
            data[fbno[1]][fbno[0]-1] += 3

    # sample #
    # data = {
    # 'User': [1,2,3,4],
    # 1: [5, 4, 0, 0],
    # 2: [0, 0, 3, 4],
    # 3: [2, 0, 0, 0],
    # }

    df = pd.DataFrame(data)
    df.set_index('User', inplace=True)

    # user = '1234'
    user_item_matrix = df
    recommend_items = user_based_recommendation(user, user_all_similarity, user_item_matrix, cnoData)
    print(recommend_items)

    conn.close()

    return recommend_items


def board_recommend(user):
    conn = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='2017018023',
                        dbname='allergydb',
                        connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT cno, username, allerinfo FROM customers""")
    cnoData = cur.fetchall()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT bno from boards""")
    bnoData = cur.fetchall()
    # print(bnoData[0:2])

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "CNO_id", "bNO_id" FROM bbookmark""")
    bbData = cur.fetchall()
    # print(choData[0:2])

    # print(cnoData[0:2])
    # 알레르기를 통한 사용자 유사도 #
    user_all_similarity = user_allergy_similarity()

    # rating 데이터 만들기 #
    data = {'User':[cno[1] for cno in cnoData]}

    for bno in bnoData:
        data[bno[0]] = [0 for _ in cnoData]

    # bookmark data 적용 #
    for bbno in bbData:
        if bbno[0] != None:
            data[bbno[1]][bbno[0]-1] += 3

    # sample #
    # data = {
    # 'User': [1,2,3,4],
    # 1: [5, 4, 0, 0],
    # 2: [0, 0, 3, 4],
    # 3: [2, 0, 0, 0],
    # }

    df = pd.DataFrame(data)
    df.set_index('User', inplace=True)
    
    # user = '1234'
    user_item_matrix = df
    recommend_items = user_based_recommendation(user, user_all_similarity, user_item_matrix, cnoData)
    print(recommend_items)

    conn.close()

    return recommend_items


def user_allergy_similarity():
    conn = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='2017018023',
                        dbname='allergydb',
                        connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT cno, username, allerinfo FROM customers""")
    cnoData = cur.fetchall()
    # print(cnoData[0:2])

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT ano, allergy FROM allergies""")
    allData = cur.fetchall()
    # print(allData[0:2])

    # 알레르기 보유를 통한 사용자 유사도 구할 data frame #
    customer_allergy_data = {'User':[cno[1] for cno in cnoData]}

    for all in allData:
        customer_allergy_data[all[0]] = [0 for _ in cnoData]

    # bookmark data 적용 #
    for cno in cnoData:
        if cno[2] != None:
            allerinfo = cno[2].strip('[]').split(', ')
            for ano in allerinfo:
                customer_allergy_data[int(ano)][cno[0]-1] = 1

    df = pd.DataFrame(customer_allergy_data)
    df.set_index('User', inplace=True)

    user_similarity = np.dot(df, df.T) / (np.linalg.norm(df, axis=1)[:, np.newaxis] * np.linalg.norm(df.T, axis=0))

    conn.close()

    return user_similarity

#=========================================================================================================================================#

# method 확인용 #
# food_recommend('1234')
# board_recommend('1234')