import csv, psycopg2, os

# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS userdata(
            rnum int not null primary key,
            gender boolean,
            older int,
            allergy text not null,
            "prdlstReportNo" varchar(20) not null,
            "prdlstNm" varchar(200) not null,
            rating int)""")

# TABLE DATA 초기화 (테스트용) #
cur.execute("""DELETE FROM userdata""")

# 필요시 주소 변경 바람 #
try:
    f = open('./UserData.csv', 'r', encoding='UTF8')
except:
    os.chdir("../")
    f = open('./allergyProject/UserData.csv', 'r', encoding='UTF8')

rdr = csv.reader(f)

for line in rdr:
    if line[0] != 'rnum':
        if line[1] == '남성':
            preUserData = ['0', line[2], line[5], line[0], line[3], line[6], line[4]]
        else:
            preUserData = ['1', line[2], line[5], line[0], line[3], line[6], line[4]]
        
        # "" 없으면 소문자로 인식 #
        cur.execute("""INSERT INTO userdata(gender, older, rating, rnum, allergy, "prdlstReportNo", "prdlstNm") values(%s, %s, %s, %s, %s, %s, %s)""", preUserData)
        conn.commit()

conn.close()
f.close()