# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import DeepLake
# from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
# from langchain.docstore.document import Document



class Retriever(): # retriver() -> Retriever()
    def __init__(self, vectorstore, input_text):
        self.vectorstore = vectorstore
        self.input_text = input_text

    # 유사도 검사. 사용자 입력 받아서 vector_store 만들 때 사용했던 청크와 임베딩 사이즈로 자동으로 처리 후 유사도 검사해줌. 
    def find_similar_documents(self, top_k =3):
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': top_k}) # 'k' : n 유사도 높은 순서대로 n 개 검색.

        return retriever