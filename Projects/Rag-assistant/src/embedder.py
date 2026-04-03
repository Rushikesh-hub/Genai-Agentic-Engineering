from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

embedding_cache = {}


def get_embeddings(texts):

    results = []

    for text in texts:

        if text in embedding_cache:
            results.append(embedding_cache[text])
        else:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )

            emb = response.data[0].embedding

            embedding_cache[text] = emb
            results.append(emb)

    return results