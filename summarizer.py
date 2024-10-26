from pdfminer.high_level import extract_text
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import concurrent.futures
import os
import time
import nltk

nltk.download('punkt')
# Initialize MongoDB client and collection
client = MongoClient('mongodb://localhost:27017/')
db = client['PDFScratcher'] 
collection = db['Summaries']

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from: {pdf_path}")
    text = extract_text(pdf_path)
    if isinstance(text, str):
        return text
    else:
        raise ValueError(f"Extracted text is not a string for {pdf_path}")

# Generate Summaries
def generate_summary(text):
    if not isinstance(text, str) or len(text) == 0:
        raise ValueError("Invalid input for summary generation.")
    print("Generating summary...")
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    total_sentences = len(list(parser.document.sentences))
    summary_length = max(1, total_sentences // 5)  # 20% of total sentences
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, summary_length)
    return ' '.join(str(sentence) for sentence in summary)

# Function to extract keywords using TF-IDF
def extract_keywords(text):
    print("Extracting keywords...")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    dense_list = dense.tolist()[0]  # Flattened list of TF-IDF scores for the document
    
    # Get keywords with non-zero scores
    keywords = [feature_names[i] for i, score in enumerate(dense_list) if score > 0]
    
    return keywords

# Function to store summaries and keywords in MongoDB
def store_summary_and_keywords(pdf_name, summary, keywords):
    print(f"Storing summary and keywords for: {pdf_name}")
    document = {
        'pdf_name': pdf_name,
        'summary': summary,
        'keywords': keywords,
        'processed_at': time.time()
    }
    collection.insert_one(document)

# Function to process PDFs
def process_pdf(pdf_path):
    try:
        print(f"Processing PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"Warning: No text extracted from {pdf_path}. Skipping.")
            return
        summary = generate_summary(text)
        keywords = extract_keywords(text)
        store_summary_and_keywords(pdf_path, summary, keywords)
        print(f"Successfully processed: {pdf_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")


class summarizer:
    # Function to read and process all PDF files in a directory with limited threads
    def process_pdfs_in_directory(directory):
        print(f"Reading PDF files from directory: {directory}")
        pdf_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdf')]
        
        # Use ThreadPoolExecutor to limit threads to 5
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_pdf, pdf_files)
