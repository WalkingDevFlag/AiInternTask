import os
import json
import PyPDF2
import pymongo

class PDFProcessor:
    def __init__(self, mongo_client, db_name, collection_name):
        self.mongo_client = mongo_client
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def ingest_pdfs(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Error: The folder path '{folder_path}' does not exist.")
            return

        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
        if not pdf_files:
            print(f"No PDF files found in '{folder_path}'.")
            return

        for filename in pdf_files:
            file_path = os.path.join(folder_path, filename)
            self.process_pdf(file_path)

    def process_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                file_size = os.path.getsize(file_path)

                length_category = self.get_length_category(num_pages)

                metadata = {
                    "document_name": os.path.basename(file_path),
                    "path": file_path,
                    "size": self.convert_size(file_size),
                    "num_pages": num_pages,
                    "length_category": length_category
                }

                self.collection.insert_one(metadata)
                print(f"Successfully processed '{metadata['document_name']}'.")

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

    def get_length_category(self, num_pages):
        if num_pages <= 10:
            return "Short"
        elif num_pages <= 30:
            return "Medium"
        else:
            return "Long"

    def convert_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 ** 2):.2f} MB"

    def save_to_json(self, output_file):
        try:
            documents = list(self.collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field
            with open(output_file, 'w') as f:
                json.dump(documents, f, indent=4)
            print(f"Metadata saved to '{output_file}'.")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
