from _chat import Chat
from _gemini import Gemini
from _vector_store import VectorStore
from _retriever import Retriever
from _crawler import Crawler

import os
from dotenv import load_dotenv


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
        article_list = crawler_.crawler()
        # data_dict = crawler_.crawling('20240419')
        # Update().update()
        # data_string = Update().dict_to_str(data_dict)

        vector_db = VectorStore().vector_store(article_list)

        while True:
            input_prompt = chat_.chat()
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
            print('----답변 드리겠습니다----')
            print(response['answer']) 
            self.output_list.append(response['answer'])



if __name__ == "__main__":
    m = Main()
    m.main()