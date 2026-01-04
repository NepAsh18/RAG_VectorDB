import os
from pypdf import PdfReader

def load_documents(base_dir):
    docs = []

    # PDFs (directly in base_dir)
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(".pdf"):
                path = os.path.join(base_dir, file)
                reader = PdfReader(path)
                text = "".join(page.extract_text() or "" for page in reader.pages)
                docs.append({
                    "filename": file,
                    "file_type": "pdf",
                    "author": reader.metadata.author if reader.metadata else None,
                    "text": text
                })
    else:
        print(f"Warning: PDF folder '{base_dir}' does not exist")

    # TXT files (optional)
    txt_dir = os.path.join(os.path.dirname(base_dir), "texts")
    if os.path.exists(txt_dir):
        for file in os.listdir(txt_dir):
            if file.endswith(".txt"):
                path = os.path.join(txt_dir, file)
                with open(path, "r", encoding="utf-8") as f:
                    docs.append({
                        "filename": file,
                        "file_type": "txt",
                        "author": None,
                        "text": f.read()
                    })

    return docs
