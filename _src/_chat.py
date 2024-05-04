# chat.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.retrievers import MergerRetriever
from _logger import Logger

class Chat():
    def __init__(self) -> None:
        self.input_prompt = ...
        self.langchain_model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.7)

    def chat(self, input_prompt):
        """
        사용자의 질문을 받는 함수. 받은 내용을 그대로 input_prompt(str) 변수에 저장
        """
        # print('----질문을 입력해주세요----')
        # print('tip : 종료를 원할 경우 "끝"을 입력해 주세요.')
        # self.input_prompt = input('User : ')
        self.input_prompt = input_prompt
        # self.input_list.append(self.input_prompt)
        
        Logger().logger(self, "success")
        return self.input_prompt

    
    def return_chain(self, retriever):
        '''
        retriever와 template을 연결해 chain으로 반환하는 함수
        '''
        template = '''
        비서처럼 정확하게 말해주되, 전반적으로 간략하게 말해줘. output은 내용이 끝날 때 마다 엔터를 쳐줘.
        chat history는 사용자의 이전 대화 내역들을 모아놓은 텍스트야. 필요할 때 잘 반영해줘
        chat history : {in_out}
        context : {context}
        input : {input} 
        answer : 
        '''
        prompt = PromptTemplate.from_template(template)
        combine_docs_chain = create_stuff_documents_chain(self.langchain_model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
        
        Logger().logger(self, "success")
        return retrieval_chain

    def merge_retriever(self, ret1, ret2):
        """
        특정한 retriever를 엮어주는 함수
        추후 return_chain함수에서 사용할 한 개의 retriever를 반환
        """
        merge_retriever = MergerRetriever(retriever=[ret1, ret2])
        Logger().logger(self, "success")
        return merge_retriever