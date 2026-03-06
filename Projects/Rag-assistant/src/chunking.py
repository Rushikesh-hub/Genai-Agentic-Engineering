def chunk_documents(documents, chunk_size=300, overlap=50):

    chunks = []

    for doc in documents:

        text = doc["content"]
        source = doc["source"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "source": source
            })

            start += chunk_size - overlap

    return chunks