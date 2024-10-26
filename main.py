import os
import json
from pymongo import MongoClient
from download import Download
from pdf import PDFProcessor
from summarizer import summarizer

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['PDFScratcher']
metadata_collection = db['PDF_Metadata']
summaries_collection = db['Summaries']

# Paths
json_path = r"E://GitHub//AI-Internship-Task//Dataset.json"          # JSON file containing PDF links
download_dir = r"E:/Random Python Scripts/wasserstoff/Dataset"           # Directory to store downloaded PDFs
output_metadata_json = "metadata.json"  # JSON file for storing metadata
output_summaries_json = "summaries.json" # JSON file for storing summaries

# Download PDFs
def download_pdfs():
    print("Starting PDF download process...")
    downloader = Download(json_path, download_dir)
    downloader.download_pdfs()
    print("All PDFs downloaded successfully.")

# Process PDFs to extract metadata and store in MongoDB and JSON
def process_and_store_metadata():
    print("Processing PDFs for metadata...")
    processor = PDFProcessor(client, 'PDFScratcher', 'PDF_Metadata')
    processor.ingest_pdfs(download_dir)

    # Save metadata to JSON
    processor.save_to_json(output_metadata_json)
    print(f"Metadata saved to JSON: {output_metadata_json}")

# Process PDFs to generate summaries and extract keywords
def process_summaries():
    print("Generating summaries and keywords...")
    summarizer.process_pdfs_in_directory(download_dir)

    # Retrieve summaries from MongoDB and save to JSON
    documents = list(summaries_collection.find({}, {"_id": 0}))
    with open(output_summaries_json, 'w') as f:
        json.dump(documents, f, indent=4)
    print(f"Summaries and keywords saved to JSON: {output_summaries_json}")

# Main function to orchestrate the tasks
def main():
    download_pdfs()
    process_and_store_metadata()
    process_summaries()
    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
