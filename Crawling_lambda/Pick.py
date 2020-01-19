import sys
import logging
import pymysql
import urllib.request
import urllib.parse
import requests
import re
import json
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    url = urllib.parse.unquote(urllib.parse.unquote(event['nowUrl']))
    item = CrawlingUtil.findApplyShop(url)

    if not item['fee']:
        item['fee'] = '0'
    
    return item
    

class CrawlingUtil:
    def crawl(url):
        req = requests.get(url)
        html = req.text
        return BeautifulSoup(html, 'html.parser')
        
    def findApplyShop(input):
            soup = CrawlingUtil.crawl(input)
            inputShoppingMall = input.split(".")[1]
            parentheses = re.compile('\(.+?\)')
            priceParsing = re.compile('[^0-9/ ]+')
            itemNameAndImg = None
            try:
                if inputShoppingMall == "11st":
                    itemNameAndImg = {'title': soup.h2.text, 'image': soup.select_one('.v-align > img').get('src'), 'price': priceParsing.sub('', soup.select_one('.sale_price').text).strip(), 'fee': priceParsing.sub('', parentheses.sub('', soup.select_one('div > .col').text)).strip(), 'link': input}
                elif inputShoppingMall == "gmarket":
                    itemNameAndImg = soup.select_one('.itemtit').text
                elif inputShoppingMall == "auction":
                    itemNameAndImg = soup.select_one('.text__item-title').text
                elif inputShoppingMall == "wemakeprice":
                    itemNameAndImg = soup.select_one('.deal_tit').text
            except AttributeError:
                itemNameAndImg = {'title':'No Content'}
            return itemNameAndImg    