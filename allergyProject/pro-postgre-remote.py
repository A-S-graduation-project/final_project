from urllib.parse import unquote
import requests, json, psycopg2, re
from similarity import food_sim

# dictionary인 prdlst를 tuple인 procData로 변경 #
def Processed(dict):
    
    rawmtrl = re.sub(r"[^\uAC00-\uD7A3a-zA-Z]", " ", dict['rawmtrl'])
    rawmtrl = rawmtrl.replace('•, \n', ' ')

    allergy_list = ','.join(allergy_trans(dict['allergy']))

    try:
        procData = (dict['prdlstReportNo'],
                    dict['prdlstNm'],
                    dict['prdkind'],
                    rawmtrl,
                    allergy_list,
                    dict['imgurl1'],
                    dict['manufacture'])
    except KeyError:
        return 0

    return procData


def allergy_trans(allergy):
    allergy_list = []
    for al in allergy.split(','):
                    translation = {
                        "대두를사용한제품과같은제조시설에서제조하고있습니다." : None,
                        "이제품은우유" : None,
                        "[d-토코페롤혼합형]" : None,
                        "해당사항없음" : None,
                        "알수 없음" : None,
                        "일수없음" : None,
                        "알수없음" : None,
                        "없음" : None,
                        "함유" : None,
                        "함류" : None,
                        "식품" : None,
                        "(" : None,
                        ")" : None,
                        "●" : None,
                        "*" : None,
                    }
                    translated = custom_make_translation(al, translation).strip()
                    if translated not in allergy_list and translated:
                        allergy_list.append(translated)
    return allergy_list


def custom_make_translation(text, translation):
    regex = re.compile('|'.join(map(re.escape, translation)))
    return regex.sub(lambda match: translation[match.group(0)], text)


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

while pageNo<=30:
    print(pageNo)
    URL = "http://apis.data.go.kr/B553748/CertImgListService/getCertImgListService"
    parameters = {"serviceKey" : unquote(serviceKey), "pageNo" : str(pageNo), "returnType" : "json"}

    try:
        res = requests.get(URL, params=parameters, verify=False, headers=headers, timeout=None)
    except Exception as ex: # error 발생 시 error의 종류 출력 후 다시 시도 #
        if ex is not ConnectionError:
            print(ex)
        continue

    try:
        data = json.loads(res.text)['body']['items']
    except: # JSONDecodeError 무시 #
        continue

    # load된 data가 없을 경우 종료 #
    if not data:
        break

    for i in data:
        prdlst = i['item']
        field = prdlst.keys()
        procData = Processed(prdlst)

        # print(procData)

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

print("\nfood_sim.py 실행")
print("========================================================================================")
food_sim()
print("========================================================================================")