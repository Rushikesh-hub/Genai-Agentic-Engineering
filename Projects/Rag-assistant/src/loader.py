import os

def load_documents(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        path = os.path.join(folder_path, file)

        if file.endswith(".txt"):

            with open(path, "r", encoding="utf-8") as f:

                text = f.read()

                documents.append({
                    "content": text,
                    "source": file
                })

    return documents