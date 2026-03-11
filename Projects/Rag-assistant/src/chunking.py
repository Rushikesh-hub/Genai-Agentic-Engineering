import nltk

nltk.download('punkt')

from nltk.tokenize import sent_tokenize


def semantic_chunk_documents(documents, max_sentences=5):

    chunks = []

    for doc in documents:

        sentences = sent_tokenize(doc["content"])

        source = doc["source"]

        for i in range(0, len(sentences), max_sentences):

            group = sentences[i:i + max_sentences]

            chunk_text = " ".join(group)

            chunks.append({
                "text": chunk_text,
                "source": source
            })

    return chunks