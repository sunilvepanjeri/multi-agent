from app.vectorstore import VectorStore


store = VectorStore()



async def retrieval_text(query: str):


    outputs = await store.query(query)

    final_data = "\n".join(outputs['documents'][0])

    return final_data


async def summarizer(query: str):

    outputs = await store.get_all_data()

    final_data = "\n".join(outputs["documents"])

    return final_data


async def data_extractor(query):

    return await retrieval_text(query)


