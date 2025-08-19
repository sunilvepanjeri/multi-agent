from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File
from tempfile import NamedTemporaryFile
from app.helper import chunk_and_store, is_valid_json, evaluation
from fastapi.responses import JSONResponse
import pymupdf
import json
from app.config import settings
from app.agent import Agent



router = APIRouter()


class Query(BaseModel):
    query: str

@router.post('/evaluate')
async def retrieve_quality(input: Query):



    responses = await evaluation(input.query.strip())


    return responses





@router.post('/chromadb/ingest/openai')
async def chroma_ingest(file: UploadFile = File(...)):

    with NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp.write(await file.read())
        tempname = tmp.name
    try:
        document = pymupdf.open(tempname)
        results = await chunk_and_store(document, chunk_size = 100, overlap = 50, model = settings.EMBEDDING_MODEL)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    return {'results': results}

@router.post('/chromadb/ingest')
async def ingest(file: UploadFile = File(...)):


    with NamedTemporaryFile(suffix= '.txt', delete = False) as tmp:
        tmp.write(await file.read())
        tempname = tmp.name
    try:
        document = pymupdf.open(tempname)
        results = await chunk_and_store(document, chunk_size = 100, overlap = 50)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    return {'results': results}



@router.post('/message-agent')
async def query(input: Query):

    query = input.query.strip()

    with open('app/bot.json', 'r') as file:
        data = json.load(file)

    agent = Agent(data)


    response = await agent.run(query)

    if isinstance(await is_valid_json(response), dict):
        response = json.loads(response)


    return {"response": response}







