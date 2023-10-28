import pymysql, psycopg2
import pandas as pd
import numpy as np
from math import sqrt

# 유사도 계산 #
def sim_person(data, allergy1, allergy2):
    sumX=0
    sumY=0
    sumPowX=0
    sumPowY=0
    sumXY=0
    count=0

    for i in data[allergy1].keys():
        if i in data[allergy2].keys():
            sumX+=data[allergy1][i]
            sumY+=data[allergy2][i]
            sumPowX+=pow(data[allergy1][i],2)
            sumPowY+=pow(data[allergy2][i],2)
            sumXY+=data[allergy1][i]*data[allergy2][i]
            count+=1

    return ( sumXY- ((sumX*sumY)/count) )/ sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count)))


# 최대 유사도 구하기 #
def top_match(data, allergy, index=3, sim_function=sim_person):
    li=[]
    for i in data:
        if allergy != i:
            li.append((sim_function(data,allergy,i), i))
    li.sort()
    li.reverse()

    return li[:index]


# 서로 다른 알레르기 간의 유사도 #
def getRecommendation (data, allergy, sim_function=sim_person):
    result = top_match(data, allergy, len(data))

    simSum=0
    score=0
    li=[]
    score_dic={}
    sim_dic={}

    for sim, al in result:
        if sim < 0 : continue
        for product in data[al].keys():
            if data[al][product] == 0:
                score += sim * data[allergy][product]
                score_dic.setdefault(product,0)
                score_dic[product] += score

                sim_dic.setdefault(product, 0)
                sim_dic[product] += sim
            
            score = 0

    for key in score_dic:
        score_dic[key] = score_dic[key]/sim_dic[key]
        if score_dic[key] != 0:
            li.append((score_dic[key],key))

    li.sort()
    li.reverse()

    return li


def food_recommend():
    # DB 연결 #
    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='2017018023',
                            dbname='allergydb',
                            connect_timeout=32768)
    cur = conn.cursor()

    # Mysql에서 DATA 읽기 (전처리 포함) #
    cur.execute("""SELECT "prdlstReportNo" FROM products""")
    proData = cur.fetchall()
    # print(proData[0:2])                                             # product data 확인용

    cur.execute("""SELECT gender,older,allergy,"prdlstReportNo",rating FROM userdata""")
    choData = cur.fetchall()
    # print(choData[0:2])                                             # user data 확인용

    # 형식 변환 #
    pdProData = pd.DataFrame(proData)
    pdChoData = pd.DataFrame(choData)

    # 병합 #
    merge_data = pd.concat([pdProData, pdChoData], join='outer')
    # print(merge_data)

    # 데이터 분포 #
    proAlData = merge_data.pivot_table(4, index=3, columns=2)       # 4 : 'rating', 3 : 'prdlstReportNo', 2: 'allergy'
    proAlData.fillna(0, inplace=True)                               # NaN -> 0
    # print(proAlData)

    # 결과 #
    # 알레르기 key가 userdata에 존재하지 않은 경우 오류 발생 #
    re = getRecommendation(proAlData, '호두, 대두, 쇠고기, 새우, 난류, 조개류, 돼지고기, 고등어')                       # userdata 수집 필요
    print(re[:10])
    print("\n")

    conn.close()

    return re

#=========================================================================================================================================#

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
    cur.execute("""SELECT "CNO_id", "bNO_id" FROM bbookmark RIGHT OUTER JOIN customers ON customers.cno = bbookmark."CNO_id" """)
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
    print(df)
    
    user_similarity = np.dot(df, df.T) / (np.linalg.norm(df, axis=1)[:, np.newaxis] * np.linalg.norm(df.T, axis=0))

    user = 1
    user_item_matrix = df
    recommend_items = user_based_recommendation(user, user_similarity, user_item_matrix)
    print(recommend_items)

    conn.close()

food_recommend()
# board_recommend()