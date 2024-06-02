from langchain.prompts import load_prompt
from langchain_community.chat_models.gigachat import GigaChat
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.chains import RetrievalQA

class Model:

    def __init__(self):
        self.credentials = 'ZmI3NGRjMDYtNTFjMC00NjdhLTljODgtNTBhOWVjMjk4M2VhOmU2NWY4YjQ2LWEwMGUtNDJjMy1iYmM5LTM0NTJkNGU0OTY3NA=='
        self.chat = GigaChat(credentials=self.credentials,  verify_ssl_certs=False)
        self.report = ''

    def setReport(self, report):
        self.report = report

    def transform(self):
        # write text to file to open later with TextLoader
        file = open("temp.txt", "w", encoding="utf-8")
        file.write(str(self.report))
        file.close()
        # Open text file
        print(f"Text length {len(self.report)}")
        loader = TextLoader("temp.txt", encoding="utf-8")
        self.documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=200,
        )
        self.documents = text_splitter.split_documents(self.documents)
        print(f"Total documents: {len(self.documents)}")

    def create_embeddings(self):
        self.embeddings = GigaChatEmbeddings(
            credentials=self.credentials, verify_ssl_certs=False
        )

        self.db = Chroma.from_documents(
            self.documents,
            self.embeddings,
            #client_settings=Settings(anonymized_telemetry=False),
            persist_directory="./chroma_db"
        )
        #self.db.persist()
        self.qa_chain = RetrievalQA.from_chain_type(self.chat, retriever=self.db.as_retriever())


    def load_chroma(self):
        self.embeddings = GigaChatEmbeddings(
            credentials=self.credentials, verify_ssl_certs=False
        )
        # load from disk
        self.db = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
        self.qa_chain = RetrievalQA.from_chain_type(self.chat, retriever=self.db.as_retriever())

    def getAnswer(self, promt):
        docs = self.db.similarity_search(promt, k=4)
        print(f"Found {len(docs)} relevant documents")
        answer = self.qa_chain({"query": promt})
        return answer

