#_vetor_store.py ver.YB
# 텍스트 data를 input으로 받고 spilit -> list를 받고 그 안에 있는 str을 split

'''
RAG를 구축하기 위해서, 텍스트 데이터를 Split하고 Vector DB에 store하는 역할을 합니다.
크롤링 결과물, 기존 대화 내역을 split하고 vector화 시켜서 DB에 저장!
https://wikidocs.net/231431
사용 메소드 : GoogleGenerativeAIEmbeddings
    임베딩:
        embed_documents: 이 메소드는 문서 객체의 집합을 입력으로 받아, 각 문서를 벡터 공간에 임베딩합니다. 주로 대량의 텍스트 데이터를 배치 단위로 처리할 때 사용됩니다.
        embed_query : 이 메소드는 단일 텍스트 쿼리를 입력으로 받아, 쿼리를 벡터 공간에 임베딩합니다. 주로 사용자의 검색 쿼리를 임베딩하여, 문서 집합 내에서 해당 쿼리와 유사한 내용을 찾아내는 데 사용됩니다.

    Vector Store
        Chroma : https://wikidocs.net/231575
        유사도 기반 검색: https://wikidocs.net/231578
'''

import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# vector_store.py
class VectorStore():
    def __init__(self):
        self.split_datas = []
        self.vector_db = None
    
    def vector_store(self, article_list):
        '''
        vector_db에 추가시키고 싶은 문장을 추가하는 메소드
        추가 후 해당 vector_db를 반환하는 메소드.
        '''

        print('crawling한 문자를 처리하고 있습니다. 잠시만 기다려주세요.')
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 500,
                chunk_overlap = 100,
            )

        for text in article_list:
            splits_text = text_splitter.split_text(text)
            self.split_datas.extend(splits_text)


        # 임베딩 모델 객체 생성
        embeddings_model = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        # split 해놓은 텍스트 데이터를 embedding한 VectorDB를 생성
        self.vector_db = Chroma.from_texts(
            self.split_datas, 
            embeddings_model,
            # collection_name = 'history',  # 저장소 구분
            # persist_directory = './db/chromadb', # 여기 블락처리
            # collection_metadata = {'hnsw:space': 'cosine'}, # l2 is the default
        )
        
        return self.vector_db
    
