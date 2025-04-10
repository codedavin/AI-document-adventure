import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from utils.config import groq_api_key, embeddings, llm

def summarize_text(text):
    try:
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="Imagine you're a master storyteller summarizing an epic tale. In 100-150 words, weave a concise, gripping summary of this text: '{text}'. Capture the heart of it with flair!"
        )
        chain = prompt_template | llm
        summary = chain.invoke({"text": text[:10000]})
        return summary.content
    except Exception as e:
        st.error(f"Summary hiccup: {e}")
        return "Couldn’t summarize—Grok took a nap!"

def store_in_chroma(text, file_name, file_order, existing_store=None):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, length_function=len)
    chunks = text_splitter.split_text(text)
    # Include file name and order in metadata
    metadatas = [{"source": file_name, "order": file_order} for _ in chunks]
    if existing_store is None:
        vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            metadatas=metadatas,
            collection_name="all_docs",
            persist_directory="./chroma_db"
        )
    else:
        existing_store.add_texts(texts=chunks, metadatas=metadatas)
        vector_store = existing_store
    vector_store.persist()
    return vector_store

def setup_qa_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"verbose": True}
    )
    return qa_chain

def decide_file(question, file_data):
    try:
        # Build context with file names, order, and summaries
        file_context = "\n".join(
            f"File: {file_name} (Order: {i + 1})\nSummary: {data['summary'] or 'No summary available'}"
            for i, (file_name, data) in enumerate(file_data.items())
        )
        last_file = list(file_data.keys())[-1] if file_data else None
        prompt_template = PromptTemplate(
            input_variables=["question", "context", "last_file"],
            template="You are an AI assistant with access to multiple files, each with an upload order (1 = first, 2 = second, etc.). Based on the question '{question}' and the following file details:\n\n{context}\n\nChoose the most relevant file to answer the question. If the question is too vague (e.g., 'read this file') or lacks specific content to determine a file, default to the last uploaded file: '{last_file}'. Return only the file name, nothing else."
        )
        chain = prompt_template | llm
        response = chain.invoke({"question": question, "context": file_context, "last_file": last_file})
        chosen_file = response.content.strip()
        if chosen_file in file_data:
            return chosen_file
        else:
            st.warning(f"LLM chose '{chosen_file}', but it’s not in the file list. Defaulting to last file: {last_file}")
            return last_file
    except Exception as e:
        st.error(f"File decision failed: {e}. Defaulting to last file: {last_file}")
        return last_file