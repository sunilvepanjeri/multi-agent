import uvicorn
from fastapi import FastAPI
from app import endpoint
from app.config import settings


app = FastAPI()

app.include_router(endpoint.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
