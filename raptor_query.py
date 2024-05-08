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
from raptor_data import raptor_pack
import argparse

CHROMA_PATH = "chroma"

# Establish a connection to the persistent storage system
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("raptor")
vector_store = ChromaVectorStore(chroma_collection=collection)

# Configure the retriever to use existing data
retriever = RaptorRetriever(
    [],
    embed_model=OpenAIEmbedding(
        model="text-embedding-3-small"
    ),
    llm=OpenAI(model="gpt-3.5-turbo", temperature=.1),
    vector_store=vector_store,  # Use the existing vector store without loading new documents
    similarity_top_k=2,  # Adjust based on your requirements
    mode="tree_traversal"  # Continue using tree traversal
)

# Initialize the query engine with the configured retriever
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1)  # Configure the language model for response generation
)

# Streamlit UI for querying
st.title("Raptor Retriever Query Interface")
query = st.text_input("Enter your query:")

if st.button("Submit"):
    response = query_engine.query(query)
    st.write("Response:", response)