# PDF Scratcher Project

This project downloads PDFs, extracts metadata, generates summaries, and performs keyword extraction. All data is stored in MongoDB and JSON files for easy access.

## Project Overview

- **`download.py`**: Downloads PDFs from URLs listed in `dataset.json`.
- **`pdf.py`**: Processes each PDF to get metadata (file size, page count, etc.).
- **`summarizer.py`**: Creates summaries and extracts keywords from each PDF.
- **`main.py`**: Coordinates the entire process: downloading, metadata extraction, summarization, and storage.

## Setup

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **MongoDB**: Make sure MongoDB is running locally on `localhost:27017`.
3. **NLTK**: Download the tokenizer data:
   ```python
   import nltk
   nltk.download('punkt')
   ```

## How to Run

1. Add PDF URLs to `dataset.json` in this format:
   ```json
   {
     "Sample1": "http://example.com/sample1.pdf",
     "Sample2": "http://example.com/sample2.pdf"
   }
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

This will:
- Download the PDFs.
- Extract metadata and save it in MongoDB (`PDF_Metadata` collection) and `metadata.json`.
- Generate summaries and keywords, storing them in MongoDB (`Summaries` collection) and `summaries.json`.

## Output

- **metadata.json**: Contains metadata (file size, page count, etc.) for each PDF.
- **summaries.json**: Contains summaries and keywords for each PDF.
