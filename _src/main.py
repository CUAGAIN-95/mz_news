from _chat import Chat
from _gemini import Gemini
from _vector_store import VectorStore
from _retriever import Retriever
from _crawler import Crawler

import os
from dotenv import load_dotenv

import streamlit as st


class Main():
    def __init__ (self):
        self.input_list = []
        self.output_list = []

    def main(self):
        if "GOOGLE_API_KEY" not in os.environ:
            load_dotenv()
            google_api_key = os.environ.get("GOOGLE_API_KEY")
        chat_ = Chat()
        gemini_ = Gemini()
        crawler_ = Crawler()

        # streamlit 실행

        st.title('Welcome to MZ-News')
        st.subheader('쉽고 빠르게 뉴스를 알려주는 chatbot, MZ-News입니다.')

        category = st.sidebar.selectbox(
            '대형 카테고리를 선택하세요.',
            ['정치', '사회', '경제', '생활 및 문화', 'IT 및 과학', '세계'  ]
        )

        st.text(f'{category} 항목 뉴스를 크롤링합니다. 잠시만 기다려주세요.')
        article_list = crawler_.crawler(category)
        vector_db = VectorStore().vector_store(article_list)

        st.text('해당 항목 뉴스 크롤링이 완료되었습니다.')
        # data_dict = crawler_.crawling('20240419')
        # Update().update()
        # data_string = Update().dict_to_str(data_dict)

        

        while True:
            user_input = st.text_input('질문을 입력하세요 : ')
            input_prompt = chat_.chat(user_input)
            if input_prompt == "끝":
                print('chatbot을 종료합니다.')
                break
            self.input_list.append(input_prompt)
  
            retriever_ = Retriever(vector_db, input_prompt)
            retriever_data = retriever_.find_similar_documents()
            
            if len(self.output_list) == 0:
                in_out = ...
            else:
                in_out_list = []
                for input_t in self.input_list:
                    in_out_list.append(input_t)
                for output_t in self.output_list:
                    in_out_list.append(output_t)
                in_out = ','.join(in_out_list)

            
            chain = chat_.return_chain(retriever_data)
            response = gemini_.gemini(chain, input_prompt, in_out)
            chat_response = response['answer']
            st.write(f'답변은 다음과 같습니다. : {chat_response}')
            self.output_list.append(chat_response)



if __name__ == "__main__":
    m = Main()
    m.main()