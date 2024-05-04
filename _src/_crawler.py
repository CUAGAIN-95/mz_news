# crawler.py

from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import pytz
import re
from _logger import Logger

class Crawler():
    def __init__(self):
        self.url_list = [] # 크롤링할 url을 모아놓는 list
        self.article_list = [] # 크롤링한 기사(str type)들을 모아놓는 리스트
        self.date = datetime.today().strftime('%Y%m%d') # 오늘 날짜 (str type)
        self.part_url_dict = {} # {소분류명 : url, 소분류명 : url... }이런 식으로 구성됨
        self.category_url = {
            '정치' : "/section/100",
            '경제' : "/section/101",
            '사회' : "/section/102",
            '생활 및 문화' : "/section/103",
            'IT 및 과학' : "/section/105",
            '세계' : "/section/104"
        }

    def crawler(self, category):
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
        main_url = 'https://news.naver.com'
        part_url = main_url + self.category_url[category]

        print(f'{category} 카테고리를 선택했습니다.')
        print(f'해당 카테고리의 기본 url은 다음과 같습니다. "{part_url}"')

        dom = BeautifulSoup(get(part_url, headers = headers).text, 'html.parser')
        part_data_list = dom.find_all('a', class_='ct_snb_nav_item_link')

        tz = pytz.timezone('Asia/Seoul')
        date_time = datetime.now(tz)
        date_text_num = date_time.strftime("%Y%m%d")

        for part_data in part_data_list:
            part_url = main_url + part_data.get('href') + '?date=' + date_text_num
            part_name = part_data.get_text()
            self.part_url_dict[part_name] = part_url
    
        print('-----------------------------------------')
        print(f' * 해당 카테고리는 다음의 소분류로 구별됩니다. * ')
        print(f"{list(self.part_url_dict.keys())}")
        print('-----------------------------------------')
    
        # step2. 소분류 카테고리별 url parsing (일단 기사가 비어있는 상황 대비 최대 15개까지 넣음)
        max = 15 # 한 소분류별 몇 개의 url까지 넣을거?
    
        for dict_k in list(self.part_url_dict.keys()):
            print(f'{dict_k} 항목 url을 parsing 합니다.')
            news_path = self.part_url_dict[dict_k]
            dom1 = BeautifulSoup(get(news_path, headers = headers).text, 'html.parser')
            news_urls = dom1.find_all('a', class_='sa_text_title', limit=max)
    
            for news_url in news_urls:
                url = news_url.get('href')
                if url not in self.url_list:
                    self.url_list.append(url)
    
            if len(self.url_list) == 0:
                print('현재 해당 카테고리와 관련된 뉴스가 없습니다.')
            else:
                print(f'{dict_k} 항목 url parsing을 완료했습니다.')
                print('-----------------------------------------')
    
        date_text_kor = date_time.strftime("%Y년 %m월 %d일")
        print(f'{date_text_kor}자 뉴스 url parse를 완료했습니다.')
        print(f'전체 리스트 개수는 {len(self.url_list)}개 입니다.')
    
        # step3. parsing한 url의 기사 내용 crawling
        print('article crawling을 진행합니다.')
        fail = 0
        for url in self.url_list:
            dom2 = BeautifulSoup(get(url, headers=headers).text, 'html.parser')
            article = dom2.find('article', class_='go_trans')
            if article is not None:
                text = re.sub(r'\|\\|\n', '', article.get_text())
                if text not in self.article_list:
                    self.article_list.append(text)
            else:
                fail = fail + 1
                print(f'해당 기사 크롤링에 {fail}번 실패했습니다.')
        
        print('-----------------------------------------')
        print('crawling이 완료되었습니다.')
        print(f'crawling을 완료한 article 개수 : {len(self.article_list)}')
        print(f'crawling을 실패한 article 개수 : {fail}')
        print('-----------------------------------------')
        
        Logger().logger(self, "success")
        return self.article_list