# vector_store.py

import os
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

class VectorStore():
    def __init__(self):
        self.split_datas = []
        self.vector_db = None
        self.embadding_function = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

    def vector_store(self, article_list, category):
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
        
        # split 해놓은 텍스트 데이터를 embedding한 VectorDB를 생성
        self.vector_db = Chroma.from_texts(
            texts=self.split_datas, 
            embedding=self.embadding_function,
            collection_name="category", # 카테고리 명으로 db 생성
            persist_directory = f'../_data/{category}', 
            # collection_metadata = {'hnsw:space': 'cosine'}, # l2 is the default
        )
        
        return self.vector_db
    
    def vector_store_load(self, category):
        print('crawling한 문자를 처리하고 있습니다. 잠시만 기다려주세요.')
        
        db_path = f"../data/{category}"
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 500,
                chunk_overlap = 100,
            )
        self.vector_db = db3 = Chroma(
            persist_directory="f'../_data/{category}", 
            embedding_function=self.embadding_function,
            )
        
        return self.vector_db
        
    