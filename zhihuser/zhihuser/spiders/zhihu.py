# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json
from zhihuser.items import UserItem
import random
headers = [
  "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
  "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
class ZhihuSpider(Spider):

    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    custom_settings={
        'DEFAULT_REQUEST_HEADERS' :{
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': random.choice(headers),
        # 'cookie': '_xsrf = IAocoSCu1vK8LtRiAzz3TApd22IPAro9;tgw_l7_route = 69f52e0ac392bb43ffb22fc18a173ee6;_zap = 3ac5ef83 - 097b - 498c - b270 - b6592ccb5675;__guid = 74140564.1529890132776811000.1534914062470.0342;q_c1 = 62ef31e794da43c688df76090e53f139 | 1534914065000 | 1534914065000;d_c0 = "ADBnmygUGA6PTkdnxCIolLH26iT87e5IhO4=|1534914065";capsion_ticket = "2|1:0|10:1534914090|14:capsion_ticket|44:MzI5YzdlMWEzN2UwNDlmOTkzNWY3YmQ2NWMwMjVmMmY=|d8598c3e39abef3aeddbd2f7447f81851fc8df6c4bf50159fde4c8819ada29e6";z_c0 = "2|1:0|10:1534914106|4:z_c0|92:Mi4xNzJta0N3QUFBQUFBUUdTTktCUVlEaVlBQUFCZ0FsVk5PanhxWEFEZndGMU8ydWZyQ1IzVVlnQWJSdE0wY2pjY0Rn|14b0a305c38d042bfee1ac522490eb1b9a48eeaa1b12363d631ffe114ee7b32e";monitor_count = 6'

    }
    }
    start_user = 'excited-vczh'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        # url='https://www.zhihu.com/api/v4/members/xiao-xi-gua-66-84?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        # url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        # yield Request(url,callback=self.parse)
        #获取单个用户信息请求
        yield Request(self.user_url.format(user=self.start_user,include =self.user_query),self.parse_user)
        #获取单个用户的关注列表
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),self.parse_fllow)
    def parse_user(self, response):
        result = json.loads(response.text)
        item=UserItem()
        #为item赋值
        for field in item.fields:
            if field in result.keys():
                item[field] =result.get(field)
        yield item
        #返回单个用户的用户列表
        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,offset =0,limit=20),self.parse_fllow)
    def parse_fllow(self,response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user = result.get('url_token'),include=self.user_query),self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.parse_fllow)
    def parse(self,response):
        print(response.text)

