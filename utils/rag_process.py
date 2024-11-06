# logic.py

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from chains.answer_check_chain2 import AnswerCheckChain2
from openai import OpenAI
import random
import re
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
client = OpenAI()

def csv_load():
    loader = CSVLoader(file_path='/Users/gim-woncheol/Desktop/nolicense_rider/SKN03-4th-3Team/data/문제 정리.csv', encoding='utf-8-sig', source_column='문제')
    return loader.load()

def process_data(data):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(data)
    return split_docs

def create_vector_db(documents):
    return FAISS.from_documents(documents=documents, embedding=embeddings)

def get_random_similar_question(query, db, k=5):
    retriever = db.as_retriever(search_kwargs={"k": k})
    similar_docs = retriever.get_relevant_documents(query)
    if similar_docs:
        return random.choice(similar_docs)
    return None

# 초기화 함수
def initialize_data():
    data = csv_load()
    split_docs = process_data(data)
    db = create_vector_db(split_docs)
    return db


answer_check_chain = AnswerCheckChain2(client)

# 문제 추출 함수
def extract_question(doc):
    content = doc.page_content
    split_text = re.split(r"(문제:|정답:|해설:|사진:)", content)
    chunks = {}
    for i in range(1, len(split_text), 2):
        field = split_text[i].strip()
        content = split_text[i + 1].strip()
        chunks[field[:-1]] = content
    return chunks