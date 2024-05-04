# main.py

from _chat import Chat
from _gemini import Gemini
from _vector_store import VectorStore
from _retriever import Retriever
from _crawler import Crawler
from _logger import Logger
import os
import shutil
from dotenv import load_dotenv
import streamlit as st

class Main():
    def __init__(self) -> None:
        self.vector_db = None
        self.db_path = "../_data/"

         
    def main(self):
        try:
            if "GOOGLE_API_KEY" not in os.environ:
                load_dotenv()
                google_api_key = os.environ.get("GOOGLE_API_KEY")

            chat_ = Chat()
            gemini_ = Gemini()
            crawler_ = Crawler()

            st.title('Welcome to MZ-News')
            st.subheader('쉽고 빠르게 뉴스를 알려주는 chatbot, MZ-News입니다.')

            category = st.sidebar.selectbox(
                '대형 카테고리를 선택하세요.',
                ['정치', '사회', '경제', '생활 및 문화', 'IT 및 과학', '세계'  ]
            )

            with st.form('form', clear_on_submit=True):
                input_prompt = st.text_input('질문을 입력하세요. : ', key='input')
                submitted = st.form_submit_button('Send')

                if submitted:
                    # pre_check1. 질문을 입력하지 않았을 때
                    if not input_prompt:
                        st.text("질문을 입력해 주세요.")
                    else:
                    # pre_check2. 질문을 정상적으로 입력
                    # _data 폴더 목록 리스트화
                        files = os.listdir(self.db_path)

                        # step1. 카테고리의 db가 _data 폴더에 있는지 체크
                        if category not in files :
                            # 1-1 없을 경우 : 카테고리 db생성
                            st.text(f'{category} 항목 뉴스를 크롤링합니다. 잠시만 기다려주세요.')
                            article_list = crawler_.crawler(category)
                            self.vector_db = VectorStore().vector_store(article_list, category=category)
                            st.text('해당 항목 뉴스 db 생성이 완료되었습니다.')
                        else:
                            # 1-2 있을 경우 : 기존의 db활용
                            st.text(f"기존에 있던 {category} 기사들을 활용합니다.")
                            self.vector_db = VectorStore().vector_store_load(category=category)

                        # step2. 카테고리 db에 대한 retriever 생성
                        retriever_ = Retriever(self.vector_db, input_prompt)
                        retriever_data = retriever_.find_similar_documents()

                        # step3. 기존의 질문에 대한 db생성 및 리트리버 결합
                        # 기존의 질문을 저장해놓은 파일이 _data에 있을 경우, flag=True반환

                        ## flag가 false이면 카테고리_input 저장한 값이 없다는 것.
                        ## 고로 처음으로 해당 카테고리를 검색했다는 소리니까 지나감
                        ## 반대로 flag가 true이면 카테고리_input 저장한 값이 있다는 거니까
                        ## 처음으로 해당 카테고리를 저장한 것이 아님.
                        ## 따라서 input, output관련 vector_db생성 + 리트리버 결합 
                        
                        flag = False
                        flag_check_path = os.path.join(self.db_path, category, '_input')

                        if flag_check_path in files:
                            flag=True

                        # 3-1 질답을 저장해 놓은 파일이 있을 경우
                        # 해당 파일을 풀어서 db 및 리트리버 생성
                        # in_out에 기존의 질답을 모두 저장
                        # 아까 만들었던 리트리버랑 엮어서 체인 생성, 질답 받음

                        if flag:
                            # 3-1-1. 기존의 질답을 불러와 db, in_out 텍스트 생성
                            print('기존의 질문과 대답을 불러와 벡터를 생성합니다.')
                            input_raw_list = []
                            output_raw_list = []
                            with open(f'../data/{category}_input', 'r', encoding='utf-8') as f:
                                for line in f:
                                    input_raw_list.append(line.strip().split(','))
                            with open(f'../data/{category}_output', 'r', encoding='utf-8') as f:
                                for line in f:
                                    output_raw_list.append(line.strip().split(','))
                            in_out_list = input_raw_list.extend(output_raw_list)
                            print(f'in_out_list : {in_out_list}')
                            in_out = ','.join(in_out_list)
                            print(in_out)
                            
                            # 3-1-2. 질답과 관련된 db 생성 (파일로 저장은 X)
                            input_db = VectorStore().vector_store_lite(input_raw_list)
                            output_db = VectorStore().vector_store_lite(output_raw_list)

                            # 3-1-3. db 기반 리트리버 생성
                            input_ret = Retriever(input_db, input_prompt)
                            in_r_data = input_ret.find_similar_documents()
                            output_ret = Retriever(output_db, input_prompt)
                            out_r_data = output_ret.find_similar_documents()
                            
                            # 3-1-4 리트리버 토대로 chain 생성 및 대답 받음
                            in_out_r = chat_.merge_retriever(in_r_data, out_r_data)
                            chain = chat_.return_chain(in_out_r)
                            response = gemini_.gemini(chain, input_prompt, in_out)
                            st.write('답변은 다음과 같습니다.\n')
                            st.write(f"{response['answer']}")
                            print(response)

                        # 3-2 저장해 놓은 질문이 없을 경우 
                        # 해당 카테고리에서 질문한건 처음이라는 소리
                        # 고로 그냥 최종적으로 체인 만들어주고 질답 받음
                        else:
                            in_out = ...
                            chain = chat_.return_chain(retriever_data)
                            response = gemini_.gemini(chain, input_prompt, in_out)
                           
                            st.write('답변은 다음과 같습니다.\n')
                            st.write(f"{response['answer']}")
                            print(response)


                        # step4. 방금 진행한 질답을 기존 파일에 이어서 작성해 저장
                        with open(f"../_data/{category}_input", 'a', encoding='utf-8') as f:
                            f.write(response['input']+'\n')
                        with open(f'../_data/{category}_output', 'a', encoding='utf-8') as f:
                            f.write(response['answer']+'\n')
                        

            Logger().logger(self, message="success")
        except Exception as e:
            Logger().logger(self, e)
        if st.button('Reset'):
            try:
                # _data 폴더 안에 있는 모든 하위 폴더 삭제
                for root, dirs, files in os.walk(self.db_path, topdown=False):
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        shutil.rmtree(dir_path)
                        print(f"{dir_path} 폴더를 삭제했습니다.")

                # _data 폴더 안에 있는 모든 txt 파일 삭제
                files = os.listdir(self.db_path)
                for file in files:
                    if file.endswith('put'):
                        file_path = os.path.join(self.db_path, file)
                        os.remove(file_path)
                        print(f'{file_path} 파일을 삭제했습니다.')
                    else:
                        pass
                st.text('성공적으로 Reset되었습니다.')
            except Exception as e:
                Logger().logger(self, e)
        st.text('꽤 오래 전에 질문을 했다면, 한 번 Reset버튼을 눌러주세요.')
        st.text('프로그램이 3분 이상 작동되지 않는다면 reset후 프로그램을 재시작해주세요.')
        
if __name__ == "__main__":

    Main().main()