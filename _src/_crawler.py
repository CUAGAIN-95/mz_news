# crawler.py

from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import re

# import time 코드 작동 시간 체크용

class Crawler():
    def __init__(self):
        self.url_list = [] # 크롤링할 url을 모아놓는 list
        self.temp_url_list = [] # 소분류에 해당되는 url을 임시로 보관. 분류별 크롤링할 애들이 15개 넘는지 확인할 목적
        self.article_list = [] # 크롤링한 기사(str type)들을 모아놓는 리스트
        self.category = int() # 카테고리 대분류
        self.date = datetime.today().strftime('%Y%m%d') # 오늘 날짜 (str type)
        self.part_url_dict = {} # {소분류명 : url, 소분류명 : url... }이런 식으로 구성됨

    def crawler(self):
        # step0. 기초 세우기
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
        main_url = 'https://news.naver.com'
        
        # step1. 대분류 카테고리 입력 및 대분류 카테고리별 소분류 카테고리 추출
        self.category = int(input('정치 : 1 / 경제 : 2, / 사회 : 3 / 생활 및 문화 : 4 / IT 및 과학 : 5 / 세계 : 6 '))
        while self.category:
            if self.category == 1: # 정치 카테고리 선택 100
                part_url = main_url + '/section/100'
                print('정치 카테고리를 선택했습니다.')
                break
            elif self.category == 2: # 경제 카테고리 선택 101
                part_url = main_url + '/section/101'
                print('경제 카테고리를 선택했습니다.')
                break
            elif self.category == 3: # 사회 카테고리 선택 102
                part_url = main_url + '/section/102'
                print('사회 카테고리를 선택했습니다.')
                break
            elif self.category == 4: # 생활 및 문화 카테고리 선택 103
                part_url = main_url + '/section/103'
                print('생활 및 문화 카테고리를 선택했습니다.')
                break
            elif self.category == 5: # IT 및 과학 카테고리 선택 105
                part_url = main_url + '/section/105'
                print('IT 및 과학 카테고리를 선택했습니다.')
                break
            elif self.category == 6: # 세계 카테고리 선택 104
                part_url = main_url + '/section/104'
                print('세계 카테고리를 선택했습니다.')
                break
            self.category = int(input('잘못된 입력입니다. 다시 입력해 주세요. '))
            
        print('해당 카테고리의 기본 url은 다음과 같습니다. ' + part_url)
        dom = BeautifulSoup(get(part_url, headers = headers).text, 'html.parser')
        part_data_list = dom.find_all('a', class_='ct_snb_nav_item_link')

        for part_data in part_data_list:
            part_url = main_url + part_data.get('href') + '?date=' + datetime.today().strftime("%Y%m%d")
            part_name = part_data.get_text()
            self.part_url_dict[part_name] = part_url
    
        print(f'해당 카테고리는 다음의 소분류로 구별됩니다. : {list(self.part_url_dict.keys())}')
        print('-----------------------------------------')
    
        # step2. 소분류 카테고리별 url parsing (일단 기사가 비어있는 상황 대비 최대 15개까지 넣음)
        max = 15 # 한 소분류별 몇 개의 url까지 넣을거?
    
        for dict_k in list(self.part_url_dict.keys()):
            print(f'{dict_k} 항목 url을 parsing 합니다.')
            news_path = self.part_url_dict[dict_k]
            dom1 = BeautifulSoup(get(news_path, headers = headers).text, 'html.parser')
            news_urls = dom1.find_all('a', class_='sa_text_title')
    
            for news_url in news_urls:
                url = news_url.get('href')
                if url not in self.url_list:
                    self.url_list.append(url)
                    self.temp_url_list.append(url)
                    if len(self.temp_url_list) == max:
                        self.temp_url_list = []
                        break
    
            if len(self.url_list) == 0:
                print('해당 카테고리와 관련된 뉴스가 없습니다. 프로그램을 다시 실행해 주세요.')
            else:
                print(f'{dict_k} 항목 url parsing을 완료했습니다.')
                print('-----------------------------------------')
    
        print(f'{datetime.today().strftime("%Y년 %m월 %d일")}자 뉴스 url parse를 완료했습니다.')
        print(f'전체 리스트 개수는 {len(self.url_list)}개 입니다.')
    
        # step3. parsing한 url의 기사 내용 crawling
        print('article crawling을 진행합니다.')
        fail = 0
        for i in range(len(self.url_list)):
            dom2 = BeautifulSoup(get(self.url_list[i], headers=headers).text, 'html.parser')
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
    
        return self.article_list
