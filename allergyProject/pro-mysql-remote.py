from urllib.parse import unquote
import requests
import json
import pymysql

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
conn = pymysql.connect(host='localhost',user='root',password='2017018023',db='allergydb',charset='utf8',connect_timeout=32768)
cur = conn.cursor()

# TABLE 생성 Query문 #
cur.execute("""CREATE TABLE IF NOT EXISTS products(
            prdlstReportNo varchar(200) NOT NULL,
            prdlstNm varchar(200),
            prdkind varchar(200),
            rawmtrl TEXT,
            allergy TEXT,
            image varchar(100),
            manufacture varchar(200),
            PRIMARY KEY (prdlstReportNo))""")

# hearder 정보 #
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

serviceKey = "KRFgFYY3tfo9A3cGfNrr%2Bzaib9lhbXTPnsWS149Apg2Vg%2Frl%2BaI9cVAVMQoMPFzLW23jYOdrysnHWISruWgzTA%3D%3D"
# TimeOut 오류시 pageNo 변경 #
pageNo = 1

while True:
    print(pageNo)
    URL = "http://apis.data.go.kr/B553748/CertImgListService/getCertImgListService"
    parameters = {"serviceKey" : unquote(serviceKey), "pageNo" : str(pageNo), "returnType" : "json"}

    # error 발생 시 error의 종류 출력 후 다시 시도 #
    try:
        res = requests.get(URL, params=parameters, verify=False, headers=headers, timeout=None)
    except Exception as ex:
        print(ex)
        continue
    
    # JSONDecodeError 무시 #
    try:
        data = json.loads(res.text)['body']['items']
    except:
        pass

    # load된 data가 없을 경우 종료 #
    if not data:
        break

    for i in data:
        prdlst = i['item']

        field = prdlst.keys()
        procData = Processed(prdlst)

        if procData:
            sql = """INSERT INTO products(prdlstReportNo, prdlstNm, prdkind, rawmtrl, allergy, image, manufacture) VALUES(%s, %s, %s, %s, %s, %s, %s)"""\
                """ON DUPLICATE KEY UPDATE prdlstNm=VALUES(prdlstNm), prdkind=VALUES(prdkind), rawmtrl=VALUES(rawmtrl), allergy=VALUES(allergy), image=VALUES(image), manufacture=VALUES(manufacture)"""
            
            # sql문의 오류가 발생한 경우 무시 #
            try:
                cur.execute(sql, procData)
                conn.commit()
            except:
                pass
        
    pageNo += 1

conn.close()