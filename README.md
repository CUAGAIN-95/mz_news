# mz_news
langchain 모델을 사용하여 뉴스를 요약해줍니다.

# 문제 정의

### 목적
- 20-30대의 포털 내 뉴스 콘텐츠 이용률 증가

### 문제
- 전체적인 뉴스 이용률 하락
- 포털 내 뉴스 콘텐츠 점유율 감소

### 목표
- 20-30대가 쉽게 접할 수 있는 매체를 활용한 뉴스 제공
- 가장 높은 뉴스 점유율을 가진 네이버 뉴스 콘텐츠를 활용한 프로그램 개발

### 기대 효과
- 20-30대의 뉴스 접근성 향상
- 네이버 내 뉴스 콘텐츠 이용률 증가

# 개발 환경
### 사용 언어
- python ≥ 3.9

### 사용 패키지
- langchain
- langchain-google-genai
- langchain-community
- langchainhub
- langchain-chroma
- bs4
- faiss-cpu
- sentence-transformers
- pytz
- os
- streamlit
- python-dotenv

### 사용 IDE
- Visual Studio Code

# mz-news 설치 및 작동 방법
### 설치하기
- 위에 작성된 패키지를 설치합니다.
- 터미널에 아래의 명령어를 입력하여 해당 Git을 저장합니다.

```
git clone https://github.com/CUAGAIN-95/mz_news.git
```

- Gemini API를 발급받습니다.
- 저장된 위치에 .env 파일을 생성한 뒤, 해당 파일에 다음과 같은 방식으로 발급 받은 Gemini API key를 입력합니다.

```python
GOOGLE_API_KEY=이곳에_발급받은_key를_입력합니다
```

- 터미널을 통해 _src 폴더에 접근한 뒤, 다음의 명령어를 터미널에 입력합니다.

```python
streamlit run main.py
```

### 챗봇 작동하기
- 알고 싶은 뉴스의 카테고리를 선택합니다.
- 챗봇에게 질문을 입력합니다.
(예 : ‘뉴스를 요약해줘’, ‘오늘 무슨 일이 있었어?’ 등)
- 챗봇이 질문에 대해 대답합니다.
- 질문을 완료했다면 Reset버튼을 눌러주세요.
- [작동예시 영상](https://youtu.be/WtBYROg6oDs)

# Trouble Shooting
| As-Is | Trouble | To-Be | Result |
| --- | --- | --- | --- |
| 모든 카테고리의 3일치 뉴스 데이터 크롤링 | 대기 시간이 오래 걸림 | 사용자가 선택하는 카테고리 뉴스 데이터만 크롤링 + 당일 뉴스 데이터만 크롤링 | 대기시간 감소  |
| 임베딩한 결과물 중 질문과 가장 가까운 1개의 결과를 반환 | 낮은 검색 정확도 | 임베딩한 결과물 중 질문과 가장 가까운 3개의 결과를 반환 | 검색 정확도 향상 |
| 터미널에서만 작동하는 프로그램 | 낮은 가시성 | streamlit을 활용한 프로토타입 개발 | 가시성 향상 |

# System Flow
![image](https://github.com/CUAGAIN-95/mz_news/assets/149945578/16012e39-70d1-406c-9e0a-0d274e10a722)


# 파일별 기능명세서
### System 영역
**`main.py`**
- 전체적인 파일 동작 총괄
- Input 및 output값, history 관리
- Streamlit 패키지 동작
- 환경 설정을 통해 gemini API 설정

**`_logger.py`**
- 모든 모듈에 log를 넣어 지난 활동을 기록함
- 작동 방식
    - 중간중간 함수에 로그를 통해 기록을 진행함
    - 실행되는 함수명을 받고 실행 결과를 출력, json file로 저장
    - 다른 파일에서 동작하는 함수의 return값 및 에러 메시지 기록
- 기록되는 내용 : 작동 시간, 실행한 클래스명, 함수명, 함수별 return값, 에러메시지

### Chat 관리 영역
**`_chat.py`**
- Chat prompt templete 설정
- LLM, Retriever를 토대로 chain을 엮어주고 return
- Input
    - Retriever : `_retriever.py`에서 받은 retriever
- 기타
    - langchain_model : 사용할 LLM을 저장할 변수

**`_gemini.py`**
- `main.py`에서 받은 input(질문)과 과거기록(in_out), 
  `_chat.py`에서 받은 chain을 토대로 API요청
- Input
    - input_prompt : 질문 내용을 저정하는 변수
    - in_out : 과거 기록(질문 및 대답)을 기록하는 변수
    - chain : `_chat.py`에서 받은 chain
- Output
    - Response : 질문 + 대답을 위해 사용한 문서 
    + 과거 기록을 활용한 gemini의 대답

**`_retriever.py`**
- 질문과 embedding값이 가장 가까운(=유사도가 가장 높은) 기사를 가지고 올 retriever 생성
- Input
    - input_text : embedding값으로 쪼갤 text
    - Vectorstore(=vector_db) : 쪼갠 text의 embedding값
- Output
    - retriever: 질문과 가장 embedding값이 가징 가까운 text를 검색하는 변수

### DB관리 영역
**`_crawler.py`**
- 사용자가 선택한 카테고리를 하나의 당일 뉴스 텍스트를 수집
- 선택 가능한 대형 카테고리 : 정치, 사회, 경제, 생활 및 문화, IT 및 과학, 세계
- 한 개의 대형 카테고리별로 상이한 소형 카테고리들이 존재함
- 한 개의 소형 카테고리당 최대 15개의 뉴스 텍스트만 수집
- 수집한 내용은 list 안에 append됨
- Input
    - Category : 사용자가 선택한 카테고리명
- Output
    - article_list : 사용자가 선택한 카테고리의 뉴스 텍스트

**`_vectorstore.py`**
- `_crawler.py`에서 return한 article_list에서 news_text를 받음
- 쪼개야 하는 news text의 embedding값을 구한 뒤, vector_db에 저장
- 저장된 db는 추후 `_retriever.py`에 전송됨
- Input
    - article_list : 쪼갤 news text list. **`_crawler.py`**와 연계됨
- Output
    - vector_db : 쪼갠 text의 embedding값 저장
- 기타
    - split_datas : 쪼갤 text를 list형태로 저장하는 곳
