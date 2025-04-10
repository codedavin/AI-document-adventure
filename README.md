
**AI Document Adventure**

Welcome to AI Document Adventure, an interactive Streamlit application that harnesses the power of artificial intelligence to unlock insights from your PDF documents! Whether you're a researcher, student, or curious explorer, this app lets you upload a PDF, generate an engaging summary, uncover the hottest topics buzzing within the text, and even ask questions to dive deeper into the content—all with a sprinkle of AI magic.

**What It Does**

- Epic Summaries: Upload a PDF, and the app crafts a gripping 100-150 word summary, narrated as if by a master storyteller. Powered by the Groq API and the LLaMA 3 model, it captures the essence of your document with flair.
- Topic Extraction: Discover what’s trending in your text! The app uses NLTK to identify the top N most frequent topics (customizable from 3 to 10), filtering out noise and presenting them with a fun frequency count.
- Question Answering: Got a burning question? The app stores your document in a Chroma vector database, enabling a RetrievalQA chain to fetch precise answers based on the content—no more skimming pages manually!
- User-Friendly Interface: Built with Streamlit, the app offers a sleek, intuitive experience with a sidebar to tweak settings and a responsive layout to showcase results.

**How to Get Started**

1. Clone the Repository: Grab the code with `git clone <repo-url>` (replace `<repo-url>` with the actual GitHub URL).
2. Install Dependencies: Run `pip install -r requirements.txt` to set up all required Python packages (listed below).
3. Launch the App: Fire it up with `streamlit run app.py` and watch the adventure unfold in your browser!

**Project Structure**

- `app.py`: The main entry point where the Streamlit UI lives.
- `utils/text_utils.py`: Handles text cleaning and topic extraction with NLTK.
- `utils/pdf_utils.py`: Extracts text from PDFs using PyPDF2.
- `utils/ai_utils.py`: Manages AI-powered summarization, vector storage, and QA functionality.
- `utils/config.py`: Stores shared configurations like API keys and model setups.
- `requirements.txt`: Lists all dependencies for easy installation.
- `.gitignore`: Keeps unnecessary files (like the Chroma DB) out of version control.

**Dependencies**

- streamlit: For the interactive web interface.
- nltk: For natural language processing tasks like tokenization and stopwords.
- PyPDF2: To extract text from PDF files.
- langchain: Powers the AI workflows, including QA and text splitting.
- langchain-groq: Integrates the Groq API for fast, powerful LLM inference.
- sentence-transformers: Provides embeddings for vector storage via HuggingFace.
- chromadb: Stores document chunks for efficient retrieval.

**Configuration Notes**

- API Key: The app uses a Groq API key for the LLaMA 3 model. Replace the placeholder in `utils/config.py` (`groq_api_key = "your-key-here"`) with your own key from groq.com.
- Persistence: The Chroma vector store saves to `./chroma_db/` for debugging, ignored by Git.

**Running the App**

Once launched, upload a PDF, tweak the sidebar options (summary, topics, number of topics), and hit "Unleash the AI!" to process your document. Results appear in a two-column layout—summary on the left, topics on the right—followed by a Q&A section to explore further.

**Contributing**

Found a bug or have an idea? Feel free to fork the repo, make changes, and submit a pull request. This project is modular by design, so it’s easy to extend—add new AI models, enhance the UI, or tweak the processing pipeline.

**License**

This project is open-source and free to use under the MIT License. Happy exploring!



