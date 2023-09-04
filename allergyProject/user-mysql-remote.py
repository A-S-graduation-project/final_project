import csv, os, pymysql

# DB 연결 #
conn = pymysql.connect(host='localhost',user='root',password='2017018023',db='allergydb',charset='utf8')
cur = conn.cursor()

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS searchapp_userdata(
            rnum int not null,
            gender text,
            older int,
            allergy text not null,
            prdlstReportNo varchar(20) not null,
            prdlstNm varchar(200) not null,
            rating int,
            PRIMARY KEY (rnum))""")

# TABLE DATA 초기화 (테스트용) #
cur.execute("""DELETE FROM searchapp_userdata""")

# 필요시 주소 변경 바람 #
f = open('allergyProject/UserData.csv', 'r', encoding='UTF8')
rdr = csv.reader(f)

for line in rdr:
    if line[0] != 'rnum':
        if line[1] == '남성':
            preUserData = [line[0], 0, line[2], line[3], line[6], line[4], line[5]]
        else:
            preUserData = [line[0], 1, line[2], line[3], line[6], line[4], line[5]]
            
        cur.execute("""INSERT INTO searchapp_userdata(rnum, gender, older, allergy, prdlstReportNo, prdlstNm, rating) values (%s, %s, %s, %s, %s, %s, %s)""", preUserData)
        conn.commit()

conn.close()
f.close()