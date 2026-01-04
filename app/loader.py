import os
from pypdf import PdfReader

def load_documents(base_dir):
    docs = []

    for file in os.listdir(f"{base_dir}/pdfs"):
        if file.endswith(".pdf"):
            reader = PdfReader(f"{base_dir}/pdfs{file}")
            text = "".join(page.extract_text() or "" for page in reader.pages)

        docs.append({
            "filename": file,
            "file_type": "pdf",
            "author": reader.metadata.author if reader.metadata else None,
            "text": text
        })

    for file in os.listdir(f"{base_dir}/texts"):
        if file.endswith(".txt"):
            with open(f"{base_dir}/texts/{file}", "r", encoding="utf-8") as f:
                docs.append({
                    "filename": file,
                    "file_type": "txt",
                    "author": None,
                    "text": f.read()
                })

    return docs    