def chunk_documents(documents, chunk_size=400, overlap=80):

    chunks = []

    for doc in documents:

        text = doc["content"]
        source = doc["source"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "source": source
            })

            start += chunk_size - overlap

    return chunks