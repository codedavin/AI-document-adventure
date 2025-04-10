import streamlit as st
from utils.text_utils import extract_topics
from utils.pdf_utils import load_pdf
from utils.ai_utils import summarize_text, store_in_chroma, setup_qa_chain, decide_file
from utils.config import groq_api_key, embeddings, llm

st.set_page_config(page_title="AI Document Adventure", page_icon="📜", layout="wide")
st.title("AI Document Adventure")
st.markdown("Upload PDFs, and let AI spin summaries, unearth topics, and answer questions across all files!")

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'file_data' not in st.session_state:
    st.session_state.file_data = {}
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'file_history' not in st.session_state:
    st.session_state.file_history = []
if 'show_qa' not in st.session_state:
    st.session_state.show_qa = False

# File upload
uploaded_file = st.file_uploader("Drop your PDF here", type="pdf")

# Handle new file upload
if uploaded_file and uploaded_file.name != st.session_state.current_file:
    st.session_state.processed = False
    st.session_state.current_file = uploaded_file.name
    if uploaded_file.name not in st.session_state.file_history:
        st.session_state.file_history.append(uploaded_file.name)
    st.session_state.show_qa = False
    st.info(f"New file detected: {uploaded_file.name}")

# Sidebar
st.sidebar.header("Tune Your Quest")
summary_toggle = st.sidebar.checkbox("Epic Summary", value=True)
topics_toggle = st.sidebar.checkbox("Uncover Hot Topics", value=True)
num_topics = st.sidebar.slider("How many topics?", 3, 10, 5) if topics_toggle else 5

# Display file sequence in sidebar
st.sidebar.header("File Sequence")
if st.session_state.file_history:
    st.sidebar.write(f"**First File**: {st.session_state.file_history[0]}")
    if len(st.session_state.file_history) > 1:
        st.sidebar.write(f"**Previous File**: {st.session_state.file_history[-2]}")
    st.sidebar.write(f"**Last File**: {st.session_state.file_history[-1]}")
    st.sidebar.write(f"**Total Files**: {len(st.session_state.file_history)}")
else:
    st.sidebar.write("No files uploaded yet.")

# Process button
if uploaded_file and st.button("Unleash the AI!") and not st.session_state.processed:
    with st.spinner("AI’s diving into the text..."):
        text = load_pdf(uploaded_file)
        if text:
            file_name = uploaded_file.name
            file_order = len(st.session_state.file_history)  # Order is the current length of history
            summary = summarize_text(text) if summary_toggle else None
            topics = extract_topics(text, num_topics) if topics_toggle else None
            st.session_state.file_data[file_name] = {'summary': summary, 'topics': topics}
            if st.session_state.vector_store is None:
                st.session_state.vector_store = store_in_chroma(text, file_name, file_order)
                st.session_state.qa_chain = setup_qa_chain(st.session_state.vector_store)
            else:
                st.session_state.vector_store = store_in_chroma(text, file_name, file_order, existing_store=st.session_state.vector_store)
            st.session_state.processed = True

# Display results for current file
if st.session_state.processed and st.session_state.current_file in st.session_state.file_data:
    col1, col2 = st.columns([2, 1])
    file_data = st.session_state.file_data[st.session_state.current_file]
    if summary_toggle and file_data['summary']:
        with col1:
            st.subheader("The Tale in a Nutshell")
            st.write(file_data['summary'])
            st.success("Summary crafted with magic!")
    if topics_toggle and file_data['topics']:
        with col2:
            st.subheader("What’s Buzzing?")
            for topic in file_data['topics']:
                st.write(f"🔥 {topic}")
            st.success(f"Top {num_topics} topics spotted!")

# QA section
st.subheader("Have a Question?")
if st.button("Ask a Question"):
    st.session_state.show_qa = True

if st.session_state.show_qa:    
    if not st.session_state.file_history:
        st.warning("No files uploaded yet. Please upload a PDF first.")
    elif st.session_state.qa_chain:
        with st.form(key='question_form'):
            question = st.text_input("What would you like to know? (LLM will choose the file)")
            submit_button = st.form_submit_button(label='Get Answer')
            if submit_button and question:
                with st.spinner("Deciding which file to query..."):
                    chosen_file = decide_file(question, st.session_state.file_data)
                    if chosen_file:
                        st.write(f"LLM chose to query: {chosen_file}")
                        with st.spinner("Searching for answers..."):
                            try:
                                retriever = st.session_state.vector_store.as_retriever(
                                    search_type="similarity",
                                    search_kwargs={"k": 5, "filter": {"source": chosen_file}}
                                )
                                st.session_state.qa_chain.retriever = retriever
                                response = st.session_state.qa_chain({"query": question})
                                st.write("Answer:", response["result"])
                                source_files = set(doc.metadata['source'] for doc in response.get('source_documents', []))
                                if source_files:
                                    st.write("Confirmed file used:", ", ".join(source_files))
                            except Exception as e:
                                st.error(f"Question-answering failed: {e}")
                    else:
                        st.error("Couldn’t decide on a file to query.")
    else:
        st.error("QA system not initialized. Process a file first.")

st.markdown("---")
st.write("Powered by AI")