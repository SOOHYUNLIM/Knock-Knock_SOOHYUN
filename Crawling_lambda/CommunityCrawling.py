import sys
import logging
import pymysql
import urllib.request
import requests
import re
import json
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    conn = pymysql.connect(host='jarvis1.clzkjwwf2qt9.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin',
                           passwd='rlxhdqks001!', db='jarvis')
    curs = conn.cursor()

    selectLastData = 'select title from tbl_community_crawling where no >= (select no from tbl_community_crawling where last_crawling = 1 order by no desc limit 1) limit 3'

    selectCategory = 'select * from tbl_category'

    addSpecialPrice = 'insert into tbl_community_crawling (category_code, title, price, fee, image, link, last_crawling) values(%s, %s, %s, %s, %s, %s, %s)'

    curs.execute(selectLastData)

    lastData = tuple(map(lambda row: row[0], curs.fetchall()))

    curs.execute(selectCategory)

    categoryMap = curs.fetchall()

    parentheses = re.compile('\(.+?\)')
    squareBrackets = re.compile('\[.+?\]')
    priceSplit = re.compile('[ /]')
    priceParsing = re.compile('[^0-9/ ]+')

    soup = BeautifulSoup("", 'html.parser')

    for i in range(1, 4):
        url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page=" + str(i) + "&divpage=58"
        html = CrawlingUtil.crawl(url)
        soup.append(html)

    items = soup.select('.list0, .list1')

    last_crawling = True

    for item in items:
        titleTag = item.select_one('.list_title')

        if not titleTag:
            continue

        titleText = titleTag.text

        title = parentheses.sub('', squareBrackets.sub('', titleText)).strip()

        if title == '':
            continue

        priceTag = squareBrackets.findall(titleText) + parentheses.findall(titleText)

        category = item.select_one('nobr.list_vspace').text

        for categoryName in categoryMap:
            if category in categoryName:
                category = categoryName[0]
                break

        link = None
        price = 0
        fee = 0

        if priceTag:
            priceArr = list(map(lambda i: 0 if i == '' else int(i), sum(map(lambda num: priceSplit.split(priceParsing.sub('', num).strip()), priceTag), [])))

            if len(priceArr) > 1:
                if 5000 >= priceArr[-1] >= 2000:
                    fee = priceArr.pop()
                price = max(priceArr)
            else:
                price = priceArr[0]

        if 10000000>= price >= 100:
            naverItem = NaverAPI.findNaverAPI(title, price)

            if not ("image" in naverItem):
                image = 'http:' + item.select_one('.thumb_border').get('src')

            else:
                image = naverItem['image']

                if int(naverItem['lprice']) < price:
                    # 배송비 추가 필요
                    title = squareBrackets.sub('', naverItem['title'])
                    price = naverItem['lprice']
                    link = naverItem['link']

            if title in lastData:
                break

            if link is None:
                boardLink = 'http://www.ppomppu.co.kr/zboard/' + item.select('a')[1].get('href')
                link = CrawlingUtil.crawl(boardLink).select_one('.wordfix a').get('href')

            curs.execute(addSpecialPrice, (category, title, price, fee, image, link, last_crawling))

            last_crawling = False

    conn.commit()


    requests.get("http://ec2-15-165-118-201.ap-northeast-2.compute.amazonaws.com:8080/kk/msg")

    return {
        'statusCode': 200,
        'body': json.dumps('Community Crawling SUCCESS')
    }


class CrawlingUtil:
    def crawl(url):
        req = requests.get(url)
        html = req.text
        return BeautifulSoup(html, 'html.parser')


class NaverAPI:
    def findSearchNaver(item):
        url = 'https://search.shopping.naver.com/' + CrawlingUtil.crawl(item['link']).select_one('script').text.strip().split("'")[1]
        info = CrawlingUtil.crawl(url).select_one('._priceListMallLogo')
        return {'title': item['title'], 'lprice': int(item['lprice']), 'mallName': info.get('data-mall-name'), 'link': info.get('href'), 'image': item['image']}

    def findNaverAPI(itemName, price):
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
        result = {'lprice': price}
        if items:
            result['image'] = items[0]['image']

        for item in items:
            item["lprice"] = int(item["lprice"])
            if result["lprice"] > item["lprice"] > price * 80 / 100:
                result = item

        if "productType" in result:
            if result["productType"] == "1":
                result = NaverAPI.findSearchNaver(result)
            result["title"] = result["title"].replace("<b>", "").replace("</b>", "")

        return result
