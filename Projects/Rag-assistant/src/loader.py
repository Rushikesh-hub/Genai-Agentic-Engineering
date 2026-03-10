import os
from PyPDF2 import PdfReader


def load_txt(path):

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def load_documents(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        path = os.path.join(folder_path, file)

        if file.endswith(".txt"):

            text = load_txt(path)

        elif file.endswith(".pdf"):

            text = load_pdf(path)

        else:
            continue

        documents.append({
            "content": text,
            "source": file
        })

    return documents