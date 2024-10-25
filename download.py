import os
import json
import requests

class Download:
    def __init__(self, json_path, download_dir):
        self.json_path = json_path
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)  

    def download_pdfs(self):
        with open(self.json_path, 'r') as file:
            pdf_links = json.load(file)

        for pdf_name, pdf_url in pdf_links.items():
            file_path = os.path.join(self.download_dir, f"{pdf_name}.pdf")
            response = requests.get(pdf_url, verify=False)  # Suppress SSL verification
            response.raise_for_status()  # Check for HTTP errors

            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)

            print(f"Downloaded: {pdf_name}.pdf")