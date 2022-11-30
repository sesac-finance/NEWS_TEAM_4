import requests
from bs4 import BeautifulSoup
import json
import time
import itertools
import pandas as pd

class Comment_crawl():
    header = {
        'authority' : 'comment.daum.net',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'accept' : "*/*",
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer' : "",
    }

    
    def comment(self, url):
        offset = 0
        temp_json_list = []

        #링크 맨 뒤 article_id 추출
        article_id = url.split("/")[-1]

        #기사 링크 들어가서 data-client-id 추출
        req = requests.get(url=url)
        soup = BeautifulSoup(req.content, 'html.parser')
        data_client_id = soup.find('div',{'class':'alex-area'}).get('data-client-id')
        self.header['referer'] = url

        #data_client_id 더해서 access token 값 추출
        token_url = "https://alex.daum.net/oauth/token?grant_type=alex_credentials&client_id={}".format(data_client_id)
        req = requests.get(token_url, headers=self.header)
        access_token = json.loads(req.content)['access_token']

        #token값 붙여서 authorize 값 완성
        authorization = 'Bearer '+access_token

        #header에 authorization 추가
        self.header['authorization'] = authorization

        #id 값 받아옴
        post_url = "https://comment.daum.net/apis/v1/ui/single/main/@{}".format(article_id)
        req = requests.get(post_url, headers = self.header)
        soup = BeautifulSoup(req.content,'html.parser')
        post_id = json.loads(soup.text)['post']['id']


        #comment url 접속해서 데이터 가져옴
        while True:
            request_url = "https://comment.daum.net/apis/v1/posts/{}/comments?parentId=0&offset={}&limit=100&sort=LATEST&isInitial=true&hasNext=true".format(post_id,offset)
            req = requests.get(request_url, headers=self.header)
            soup = BeautifulSoup(req.content,'html.parser')
            temp_json_list.append(json.loads(soup.text))
            
            if len(temp_json_list) < 100:
                break
            else:
                offset += 100
                time.sleep(1)

        temp_json_list = list(itertools.chain(*temp_json_list))

        return self.comment_view(temp_json_list, url), self.action_crawl(article_id)
    
    def action_crawl(self, article_id):
        re_url = 'https://action.daum.net/apis/v1/reactions/home?itemKey={}'.format(article_id)
        req = requests.get(re_url, headers=self.header)
        soup = BeautifulSoup(req.content,'html.parser')
        action = json.loads(soup.text)['item']['stats']
        df = pd.DataFrame({'like' : action['LIKE'], 'dislike' : action['DISLIKE'],'great' : action['GREAT'],'sad' : action['SAD'],
                            'absurd' : action['ABSURD'],'angry' : action['ANGRY'],'recommend' : action['RECOMMEND'],'impress' : action['IMPRESS']}, index = [0])
        return df
        
        
            

    def comment_view(self, comment_list, url):
        comm, user_id, date, urls =[],[],[],[]
        for comment in comment_list:
            comm.append(comment['content'])
            user_id.append(comment['user']['id'])
            date.append(comment['createdAt'])
            urls.append(url)
        
        # print(comm, user_id, date)
        df = pd.DataFrame({'user_id': user_id,'date':date, 'content': comm, 'url': urls})
        print(df)
        return df

com = Comment_crawl()
url = 'https://v.daum.net/v/20221130112503994'
com.comment(url)


