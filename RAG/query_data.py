import streamlit as st
import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from llama_index.packs.raptor import RaptorPack

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Streamlit interface instead of CLI.
    query_text = st.text_input("Enter your query:", "")

    if st.button("Search"):
        # Prepare the DB.
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_relevance_scores(query_text, k=3)

        if len(results) == 0 or results[0][1] < 0.7:
            st.write("Unable to find matching results.")
            return

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI()
        response_text = model.predict(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        st.write(formatted_response)
    
    st.subheader("General Chat")
    chat_text = st.text_input("Chat with the bot:", "")
    if st.button("Chat"):
        if chat_text:
            model = ChatOpenAI()
            response_text = model.predict(chat_text)
            st.write(f"Bot says: {response_text}")

if __name__ == "__main__":
    st.title("Phillipe's NBA Bet Helper")
    main()