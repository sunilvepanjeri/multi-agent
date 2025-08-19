from chromadb import PersistentClient
from app.config import settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os



class VectorStore:

    def __init__(self, **kwargs):

        if len(kwargs):
            self.chroma_client = PersistentClient(path = './openai')
            self.collection = self.chroma_client.get_or_create_collection(
            name='embedd',
            embedding_function=OpenAIEmbeddingFunction(
                model_name = kwargs.get('model'),
                api_key = os.getenv("OPENAI_API_KEY")
                )
            )
        else:
            self.chroma_client = PersistentClient(path = './sentence_transformer')
            self.collection = self.chroma_client.get_or_create_collection(name = settings.COLLECTION_NAME)


    async def index_data(self, insert_data):

        self.collection.upsert(
            documents = insert_data,
            ids = ['id' + str(i) for i in range(len(insert_data))],
        )

        return 'successfully indexed data'

    async def query(self, query):

        if isinstance(query, str):
            query = [query]

        results = self.collection.query(
            query_texts=query,
            n_results = 2
        )

        return results
    async def get_all_data(self):

        results = self.collection.get()

        return results