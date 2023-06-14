import os
import streamlit as st

from enum import Enum
from typing import NewType

from file_manager import get_dataset_text


# load api secrets
key = st.secrets.api_key
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


Dataset = NewType("Dataset", int)
class Datasets(Enum):
    ALL = Dataset(0)
    FRESHMAN = Dataset(1)
    SOPHOMORE = Dataset(2)
    JUNIOR = Dataset(3)
    SENIOR = Dataset(4)


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
    texts = splitter.split_text(get_dataset_text(dataset))
    embeddings = OpenAIEmbeddings()
    search_index = Chroma.from_texts(texts, embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(model="text-ada-001", temperature=temperature), 
        chain_type=model, retriever=search_index.as_retriever())

    return qa.run(query)
