import pymysql
import urllib.request
import requests
import json
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    conn = pymysql.connect(host='jarvis1.clzkjwwf2qt9.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin',
                           passwd='rlxhdqks001!', db='jarvis', cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

    selectPickList = 'select pno, title, wanted_price from tbl_pick where receipt = true'

    addLowPrice = 'insert into tbl_lowprice (pno, category_code, title, price, fee, image, link) values(%s, %s, %s, %s, %s, %s, %s)'

    updateState = 'update tbl_pick set state = true where pno = %s'

    curs.execute(selectPickList)

    pickList = curs.fetchall()

    for pick in pickList:
        item = NaverAPI.findNaverAPI(pick['title'])
        curs.execute(addLowPrice, (pick['pno'], None, item['title'], item['price'], item['fee'], item['image'], item['link']))
        if int(item['price']) < pick['wanted_price']:
            curs.execute(updateState, pick['pno'])

    conn.commit()
    requests.get("http://ec2-15-165-118-201.ap-northeast-2.compute.amazonaws.com:8080/kk/lprice")
    # return 200


class CrawlingUtil:
    def crawl(url):
        req = requests.get(url)
        html = req.text
        return BeautifulSoup(html, 'html.parser')


class NaverAPI:
    def findSearchNaver(item):
        url = 'https://search.shopping.naver.com/' + \
              CrawlingUtil.crawl(item['link']).select_one('script').text.strip().split("'")[1]
        info = CrawlingUtil.crawl(url).select_one('._priceListMallLogo')
        item['mallName'] = info.get('data-mall-name')
        item['link'] = info.get('href')
        return item

    def findNaverAPI(itemName):
        url = "https://openapi.naver.com/v1/search/shop?query=" + urllib.parse.quote(itemName)  # json 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", "NrksAQQEffia0Ek4iYdi")
        request.add_header("X-Naver-Client-Secret", "dopvU8BXFH")
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
        else:
            print("Error Code:" + rescode)

        items = json.loads(response_body)["items"]
        result = items[0] if items else {'title': '결과가 없습니다!'}

        if items is None:
            return result

        for item in items:
            result = item if int(item["lprice"]) < int(result["lprice"]) else result

        if result["productType"] == "1":
            result = NaverAPI.findSearchNaver(result)

        result["title"] = result["title"].replace("<b>", "").replace("</b>", "")
        result["price"] = result.pop("lprice")
        result["fee"] = 0

        return result