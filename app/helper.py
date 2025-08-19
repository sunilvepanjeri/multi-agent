from app.vectorstore import VectorStore
from pydantic import BaseModel, Field
import json
from openai import OpenAI
from app.config import settings
import time

client = OpenAI()

async def chunk_and_store(file, chunk_size = 100, overlap = 50, **kwargs):

    documents = []

    for doc in file:
        text = doc.get_text()
        text = text.strip().split()
        for start in range(0, len(text), chunk_size):
            if not documents:
                documents.append(" ".join(text[start : chunk_size]))
            else:
                documents.append(" ".join(text[start - overlap : start + chunk_size]))

    if kwargs.get('model'):
        vector_db = VectorStore(model = kwargs.get('model'))
    else:

        vector_db = VectorStore()

    result = await vector_db.index_data(documents)

    return result


async def is_valid_json(response):

    try:
        return json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return None


class Metric(BaseModel):
    better_model: str = Field(description="predict which embedding model retrieved the right chunks")

async def evaluation(query: str):

    openai_embedding = VectorStore(model="text-embedding-3-small")
    sentence_transformer = VectorStore()

    intial_openai = time.perf_counter()
    openai_results = await openai_embedding.query(query)
    final_time_openai = time.perf_counter() - intial_openai

    intial_time = time.perf_counter()
    generic_results = await sentence_transformer.query(query)
    final_generic_time = time.perf_counter() - intial_time


    response = client.responses.parse(
        model = settings.MODEL,
        input = [{"role": "system", "content": "You are world class Classifier to find which embedding model retrieved the right chunks"},
            {
                "role": "user",
                "content": f"This the data retrieved from chromadb default sentence transformer model - {generic_results}.Time taken for retrieval {final_generic_time}"
            },
            {
                "role": "user",
                "content": f"This are chunks retrieved from the chroma openai functions model - {openai_results}.Time taken for retrieval {final_time_openai}"
            }],
        text_format = Metric
    )

    output_json = {'best_embedding_model': response.output_parsed, 'openai_time': final_time_openai, 'generic_sentence_transformer_time': final_generic_time}

    return output_json









