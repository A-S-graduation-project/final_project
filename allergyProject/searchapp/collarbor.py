import pymysql, psycopg2
import pandas as pd
import numpy as np


def user_based_recommendation(user, user_similarity, user_item_matrix):
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
            if user_item_matrix.at[user, item] == 0 and user_item_matrix.at[user_id+1, item] > 0:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += similarity_score * user_item_matrix.at[user_id+1, item]
    
    # Sort the recommendations by score in descending order
    recommendations = dict(sorted(recommendations.items(), key=lambda x: x[1], reverse=True))
    
    return recommendations


#=========================================================================================================================================#

def food_recommend():
    # DB 연결 #
    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='2017018023',
                            dbname='allergydb',
                            connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT cno FROM customers""")
    cnoData = cur.fetchall()
    # print(cnoData[0:2])

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "prdlstReportNo" FROM products""")
    proData = cur.fetchall()
    # print(proData[0:2])

    cur.execute("""SELECT "CNO_id", "FNO_id" FROM fbookmark""")
    choData = cur.fetchall()
    # print(choData[0:2])

    # 기초 데이터 만들기 #
    data = {'User':[cno[0] for cno in cnoData]}

    for pro in proData:
        data[pro[0]] = [0 for _ in cnoData]

    # bookmark data 적용 #
    for cho in choData:
        if cho[0] != None:
            data[cho[1]][cho[0]-1] += 3

    df = pd.DataFrame(data)
    df.set_index('User', inplace=True)
    
    user_similarity = np.dot(df, df.T) / (np.linalg.norm(df, axis=1)[:, np.newaxis] * np.linalg.norm(df.T, axis=0))

    user = 1
    user_item_matrix = df
    recommend_items = user_based_recommendation(user, user_similarity, user_item_matrix)
    print(recommend_items)

    # # 형식 변환 #
    # pdProData = pd.DataFrame(proData)
    # pdChoData = pd.DataFrame(choData)

    # # 병합 #
    # merge_data = pd.concat([pdProData, pdChoData], join='outer')
    # # print(merge_data)

    # # 데이터 분포 #
    # proAlData = merge_data.pivot_table(4, index=3, columns=2)       # 4 : 'rating', 3 : 'prdlstReportNo', 2: 'allergy'
    # proAlData.fillna(0, inplace=True)                               # NaN -> 0
    # # print(proAlData)

    # # 결과 #
    # # 알레르기 key가 userdata에 존재하지 않은 경우 오류 발생 #
    # re = getRecommendation(proAlData, '호두, 대두, 쇠고기, 새우, 난류, 조개류, 돼지고기, 고등어')                       # userdata 수집 필요
    # print(re[:10])
    # print("\n")

    conn.close()

#=========================================================================================================================================#

def board_recommend():
    # DB 연결 #
    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='2017018023',
                            dbname='allergydb',
                            connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT cno from customers""")
    cnoData = cur.fetchall()
    # print(cnoData[0:2]) 

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT bno from boards""")
    bnoData = cur.fetchall()
    # print(bnoData[0:2])

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "CNO_id", "bNO_id" FROM bbookmark""")
    choData = cur.fetchall()
    # print(choData[0:2])

    # 기초 데이터 만들기 #
    data = {'User':[cno[0] for cno in cnoData]}

    for bno in bnoData:
        data[bno[0]] = [0 for _ in cnoData]

    # bookmark data 적용 #
    for cho in choData:
        if cho[0] != None:
            data[cho[1]][cho[0]-1] += 3

    # sample #
    # data = {
    # 'User': [1,2,3,4],
    # 1: [5, 4, 0, 0],
    # 2: [0, 0, 3, 4],
    # 3: [2, 0, 0, 0],
    # }

    df = pd.DataFrame(data)
    df.set_index('User', inplace=True)
    
    user_similarity = np.dot(df, df.T) / (np.linalg.norm(df, axis=1)[:, np.newaxis] * np.linalg.norm(df.T, axis=0))

    user = 1
    user_item_matrix = df
    recommend_items = user_based_recommendation(user, user_similarity, user_item_matrix)
    print(recommend_items)

    conn.close()

# food_recommend()
# board_recommend()