from src.embedder import get_embeddings
from src.search import search
from src.prompt_template import build_prompt
from src.generator import generate_answer


def run_rag(index, chunks, question):

    query_embedding = get_embeddings([question])[0]

    indices = search(index, query_embedding)

    retrieved_chunks = [chunks[i] for i in indices]

    prompt = build_prompt(retrieved_chunks, question)

    answer = generate_answer(prompt)

    return answer, retrieved_chunks