from llama_index.packs.raptor import RaptorPack
import os
import streamlit as st
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.packs.raptor import RaptorRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
import chromadb

CHROMA_PATH = "chroma"
DATA_PATH = "data/stats"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
openai_api_key= os.getenv('openai_api_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

document= SimpleDirectoryReader(input_files=["/Users/phill/RAG-model/data/stats/nba_data.md"]).load_data()

client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection("raptor")

vector_store = ChromaVectorStore(chroma_collection=collection)

raptor_pack = RaptorPack(
    document,
    embed_model=OpenAIEmbedding(
        model="text-embedding-3-small"
    ),
    llm=OpenAI(model="gpt-3.5-turbo", temperature=.01),  #used for generating sumaries
    vector_store=vector_store, #used for storage
    similarity_top_k=2,  # Top k for each layer, or overall top-k for collapsed
    mode="collapsed",  #  sets default mode
    transformations=[
        SentenceSplitter(chunk_size=1500, chunk_overlap=150)
    ],
)
