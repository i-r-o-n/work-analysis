import os
import json

key = json.load(open("key.json"))["api key"]
os.environ["OPENAI_API_KEY"] = key

from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader

with open("1.txt") as f1:
    y1 = f1.read()
with open("2.txt") as f2:
    y2 = f2.read()
with open("3.txt") as f3:
    y3 = f3.read()
with open("4.txt") as f4:
    y4 = f4.read()


# source_chunks = []
# splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)

# for chunk in splitter.split_text(y1):
#     source_chunks.append(Document(page_content=chunk))

# search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings())
# loader = TextLoader("1.txt")
# splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )
# documents = loader.load()
# texts = splitter.split_documents(documents) 
texts = splitter.split_text(y2)

embeddings = OpenAIEmbeddings()

docsearch = Chroma.from_texts(texts, embeddings)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.6), 
    chain_type="map_reduce", retriever=docsearch.as_retriever())

query = "What is the most thought-provoking idea in this text?"
print(qa.run(query))


