import os
import json

from enum import Enum
from typing import NewType

# load api secrets
key = json.load(open("key.json"))["api key"]
os.environ["OPENAI_API_KEY"] = key

from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA


Model = NewType("Model", str)
class ModelTypes(Enum):
    STUFF = Model("stuff")
    MAP_REDUCE = Model("map_reduce")
    REFINE = Model("refine")
    MAP_RERANK = Model("map_rerank")


Dataset = NewType("Dataset", str)
class Datasets(Enum):
    ALL = 0
    FRESHMAN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4


class Defaults:
    temperature = 0.7,
    model = ModelTypes.MAP_REDUCE


def make_query(
        query: str, 
        dataset: Dataset = Datasets.ALL.value, 
        temperature: float = Defaults.temperature, 
        model: Model = ModelTypes.MAP_REDUCE.value) -> str:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"]) 
    texts = splitter.split_text(dataset)
    embeddings = OpenAIEmbeddings()
    search_index = Chroma.from_texts(texts, embeddings)
    # model = "text-ada-001"
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=temperature), 
        chain_type=model, retriever=search_index.as_retriever())

    return qa.run(query)
