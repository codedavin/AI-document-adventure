from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings

groq_api_key = "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"
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")