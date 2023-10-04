from urllib.parse import unquote
import requests, json, psycopg2, re

# dictionary인 prdlst를 tuple인 procData로 변경 #
def Processed(dict):
    try:
        procData = (dict['prdlstReportNo'],
                    dict['prdlstNm'],
                    dict['prdkind'],
                    dict['rawmtrl'],
                    dict['allergy'],
                    dict['imgurl1'],
                    dict['manufacture'])
    except KeyError:
        return 0

    # 확인용 #
    # print(procData)

    return procData


# DB 연결 #
conn = psycopg2.connect(host='localhost',user='postgres',password='2017018023',dbname='allergydb',connect_timeout=32768)
cur = conn.cursor()

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS products(
            "prdlstReportNo" varchar(50) NOT NULL primary key,
            "prdlstNm" varchar(200) NOT NULL,
            prdkind varchar(200) NOT NULL,
            rawmtrl TEXT NOT NULL,
            allergy TEXT,
            image varchar(100),
            manufacture varchar(200))""")

# hearder 정보 #
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

serviceKey = "KRFgFYY3tfo9A3cGfNrr%2Bzaib9lhbXTPnsWS149Apg2Vg%2Frl%2BaI9cVAVMQoMPFzLW23jYOdrysnHWISruWgzTA%3D%3D"
# TimeOut 오류시 pageNo 변경 #
pageNo = 1

while True:
    print(pageNo)
    URL = "http://apis.data.go.kr/B553748/CertImgListService/getCertImgListService"
    parameters = {"serviceKey" : unquote(serviceKey), "pageNo" : str(pageNo), "returnType" : "json"}

    try:
        res = requests.get(URL, params=parameters, verify=False, headers=headers, timeout=None)
    except Exception as ex: # error 발생 시 error의 종류 출력 후 다시 시도 #
        print(ex)
        continue

    try:
        data = json.loads(res.text)['body']['items']
    except: # JSONDecodeError 무시 #
        pass

    # load된 data가 없을 경우 종료 #
    if not data:
        break

    for i in data:
        prdlst = i['item']
        field = prdlst.keys()

        try:
            procData = list(Processed(prdlst))
            procData[3] = re.sub(r"[^\uAC00-\uD7A3a-zA-Z]", " ", procData[3])
            procData[3] = procData[3].replace('•, \n', ' ')
            procData = tuple(procData)
        except: # TypeError 방지 #
            pass

        procData = Processed(prdlst)

        if procData:
            # "" 없으면 소문자로 인식 #
            sql = """INSERT INTO products("prdlstReportNo", "prdlstNm", prdkind, rawmtrl, allergy, image, manufacture)"""\
                """VALUES(%s, %s, %s, %s, %s, %s, %s)"""\
                """ON CONFLICT ("prdlstReportNo")"""\
                """DO UPDATE SET "prdlstNm" = EXCLUDED."prdlstNm", prdkind=EXCLUDED.prdkind, rawmtrl=EXCLUDED.rawmtrl, allergy=EXCLUDED.allergy, image=EXCLUDED.image, manufacture=EXCLUDED.manufacture"""
            
            try:
                cur.execute(sql, procData)
                conn.commit()
            except Exception as ex: # sql문의 오류가 발생한 경우 무시 #
                conn.commit()
                print(ex)
                pass
        
    pageNo += 1

conn.close()