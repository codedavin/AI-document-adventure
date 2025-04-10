import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def clean_text(text):
    text = re.sub(r'[^\x20-\x7E]', ' ', text)  # Keep printable ASCII
    return re.sub(r'\s+', ' ', text).strip()

def extract_topics(text, top_n=5):
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(words).most_common(top_n)
    return [f"{word} (buzzing {freq} times)" for word, freq in word_freq]