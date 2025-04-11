

**AI Document Adventure**

Welcome to AI Document Adventure, an interactive Streamlit application that leverages artificial intelligence to unlock insights from your PDF documents! Whether you're a researcher, student, or curious mind, this app lets you upload PDFs, generate captivating summaries, uncover trending topics, and ask questions with a sophisticated contextual Retrieval-Augmented Generation (RAG) system—all powered by cutting-edge AI.

**What It Does**

- Epic Summaries: Upload a PDF, and the app crafts a gripping 100-150 word summary, narrated as if by a master storyteller. Powered by the Groq API and the LLaMA 3 model, it distills your document with flair.
- Topic Extraction: Discover what’s buzzing! Using NLTK, the app identifies the top N topics (customizable from 3 to 10), filtering noise and presenting them with frequency counts.
- Contextual RAG Question Answering: Ask anything about your documents! The app stores all uploaded files in a single Chroma vector store with metadata (file name and upload order). An LLM decides the most relevant file based on your question, file summaries, and sequence, then retrieves and answers using only that file’s context—no manual file selection needed.
- File Sequence Tracking: Keep tabs on your uploads! The app tracks the order of files (first, previous, last) and displays it in the sidebar, syncing this sequence with the RAG system for queries like "What’s in the first file?"
- User-Friendly Interface: Built with Streamlit, it offers a sleek, intuitive experience with a sidebar to tweak settings and a responsive layout for results.

**How to Get Started**

1. Clone the Repository: Grab the code with `git clone <repo-url>` (replace `<repo-url>` with the actual GitHub URL).
2. Install Dependencies: Run `pip install -r requirements.txt` to set up all required Python packages (listed below).
3. Launch the App: Fire it up with `streamlit run app.py` and explore in your browser!

**Project Structure**

- `app.py`: The main entry point for the Streamlit UI and logic.
- `utils/text_utils.py`: Handles text cleaning and topic extraction with NLTK.
- `utils/pdf_utils.py`: Extracts text from PDFs using PyPDF2.
- `utils/ai_utils.py`: Manages AI functions—summarization, vector storage with sequence metadata, and contextual file selection for RAG.
- `utils/config.py`: Stores shared configurations like API keys and model setups.
- `requirements.txt`: Lists all dependencies for easy installation.
- `.gitignore`: Excludes unnecessary files (e.g., Chroma DB) from version control.

**Dependencies**

- streamlit: For the interactive web interface.
- nltk: For natural language processing tasks like tokenization and stopwords.
- PyPDF2: To extract text from PDF files.
- langchain: Powers the AI workflows, including RAG and text splitting.
- langchain-groq: Integrates the Groq API for fast LLM inference.
- sentence-transformers: Provides embeddings via HuggingFace for vector storage.
- chromadb: Stores document chunks with metadata for efficient retrieval.

Configuration Notes**

- API Key: Replace the `groq_api_key` in `utils/config.py` with your own key from groq.com.
- Persistence: The Chroma vector store saves to `./chroma_db/` for debugging, ignored by Git.

Running the App

Launch the app, upload PDFs, tweak sidebar options (summary, topics, number of topics), and click "Unleash the AI!" to process each file. Results show the current file’s summary and topics. In the QA section, ask questions like "What’s in the first file?" or "What is AI?"—the LLM will choose the file based on order and content, delivering precise answers from that file’s context.

Key Features of Contextual RAG

- Sequence-Aware: Files are tagged with upload order (e.g., 1 for first, 2 for second) in the vector store metadata, enabling queries about specific positions (e.g., "second file").
- Smart File Selection: The LLM analyzes the question, file summaries, and upload order to pick the most relevant file. Vague queries (e.g., "read this file") default to the last uploaded file.
- Focused Retrieval: Answers come only from the chosen file’s chunks, ensuring contextually relevant responses without cross-file confusion.

Contributing

Found a bug or have an idea? Fork the repo, make changes, and submit a pull request. The modular design makes it easy to extend—add new AI models, enhance the RAG system, or refine the UI.

License

This project is open-source and free to use under the MIT License. Dive in and explore!

---

### Changes Made
1. **Contextual RAG Section**: Added a detailed description under "What It Does" and a new "Key Features of Contextual RAG" section to highlight the sequence tracking, smart file selection, and focused retrieval you’ve implemented.
2. **Sequence Tracking**: Emphasized how file order is tracked and要件

Truncated end of this file is truncated to avoid exceeding character limits. The full version includes all sections as described. Let me know if you need the rest!