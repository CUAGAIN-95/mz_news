# vector_store.py


# import os
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from _logger import Logger

class VectorStore():
    def __init__(self):
        self.split_datas = []
        self.vector_db = None
        self.embadding_function = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

    def vector_store(self, article_list, category):
        print('crawling한 기사를 처리하고 있습니다. 잠시만 기다려주세요.')

        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100
            )
        
        for text in article_list:
            splits_text = text_splitter.split_text(text)
            self.split_datas.extend(splits_text)

        self.vector_db = Chroma.from_texts(
            texts=self.split_datas, 
            embedding=self.embadding_function,
            collection_name="category", # 카테고리 명으로 db 생성
            persist_directory = f'../_data/{category}', 
            # collection_metadata = {'hnsw:space': 'cosine'}, # l2 is the default
        )
        Logger().logger(self, "success")
        return self.vector_db
    
    def vector_store_lite(self, text_list):
        '''
        굳이 db로 저장하지 않고 일회용으로 간단하게 활용할 vectordb생성
        저장해놓은 input자료와 output자료를 vectordb로 만들 때 사용
        '''
        print('crawling한 기사를 처리하고 있습니다. 잠시만 기다려주세요.')

        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100
            )
        
        for text in text_list:
            splits_text = text_splitter.split_text(text)
            self.split_datas.extend(splits_text)

        self.vector_db = Chroma.from_texts(
            texts=self.split_datas, 
            embedding=self.embadding_function,
            collection_name="category" # 카테고리 명으로 db 생성
            # persist_directory = f'../_data/{category}', 
            # collection_metadata = {'hnsw:space': 'cosine'}, # l2 is the default
        )
        Logger().logger(self, "success")
        return self.vector_db
    
    def vector_store_load(self, category):
        """
        이전에 만들어놓은 db를 load하는 함수
        """
        db_path = f"../_data/{category}"
        
        print("기존의 crawling한 기사들을 처리하고 있습니다. 잠시만 기다려주세요.")
        self.vector_db = Chroma(
            persist_directory=db_path,
            embedding_function=self.embadding_function
        )
        Logger().logger(self, "success")
        return self.vector_db