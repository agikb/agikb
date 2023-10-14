import os

from wasabi import msg  # type: ignore[import]

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path
from pydantic import BaseModel

from agikb.simple_engine import SimpleAgikbQueryEngine
from agikb.advanced_engine import AdvancedAgikbQueryEngine

from dotenv import load_dotenv

load_dotenv()

# agikb_engine = SimpleAgikbQueryEngine()
agikb_engine = AdvancedAgikbQueryEngine()

# FastAPI App
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://agikb-golden-ragtriever.onrender.com",
    "http://localhost:8000",
]

# Add middleware for handling Cross Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent



class QueryPayload(BaseModel):
    query: str


class GetDocumentPayload(BaseModel):
    document_id: str


# @app.get("/")
# async def serve_frontend():
#     return FileResponse(os.path.join(BASE_DIR, "frontend/out/index.html"))


# Define health check endpoint
@app.get("/api/health")
async def root():
    try:
        if agikb_engine.get_client().is_ready():
            return JSONResponse(
                content={
                    "message": "Alive!",
                }
            )
        else:
            return JSONResponse(
                content={
                    "message": "Database not ready!",
                },
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
    except Exception as e:
        msg.fail(f"Healthcheck failed with {str(e)}")
        return JSONResponse(
            content={
                "message": f"Healthcheck failed with {str(e)}",
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


# Define health check endpoint
@app.get("/api/get_google_tag")
async def get_google_tag():
    tag = os.environ.get("AGIKB_GOOGLE_TAG", "")

    if tag:
        msg.good("Google Tag available!")

    return JSONResponse(
        content={
            "tag": tag,
        }
    )


# Receive query and return chunks and query answer
@app.post("/api/query")
async def query(payload: QueryPayload):

    print('payload',payload)
    try:
        system_msg, results = agikb_engine.query(
            payload.query, os.environ["AGIKB_MODEL"]
        )
        msg.good(f"Succesfully processed query: {payload.query}")

        return JSONResponse(
            content={
                "system": system_msg,
                "documents": results,
            }
        )
    except Exception as e:
        msg.fail(f"Query failed")
        print(e)
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )


# Retrieve auto complete suggestions based on user input
@app.post("/api/suggestions")
async def suggestions(payload: QueryPayload):
    try:
        suggestions = agikb_engine.get_suggestions(payload.query)

        return JSONResponse(
            content={
                "suggestions": suggestions,
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "suggestions": [],
            }
        )


# Retrieve specific document based on UUID
@app.post("/api/get_document")
async def get_document(payload: GetDocumentPayload):
    msg.info(f"Document ID received: {payload.document_id}")

    try:
        document = agikb_engine.retrieve_document(payload.document_id)
        msg.good(f"Succesfully retrieved document: {payload.document_id}")
        return JSONResponse(
            content={
                "document": document,
            }
        )
    except Exception as e:
        msg.fail(f"Document retrieval failed: {str(e)}")
        return JSONResponse(
            content={
                "document": {},
            }
        )


## Retrieve all documents imported to Weaviate
@app.post("/api/get_all_documents")
async def get_all_documents():
    msg.info(f"Get all documents request received")

    try:
        documents = agikb_engine.retrieve_all_documents()
        msg.good(f"Succesfully retrieved document: {len(documents)} documents")
        return JSONResponse(
            content={
                "documents": documents,
            }
        )
    except Exception as e:
        msg.fail(f"All Document retrieval failed: {str(e)}")
        return JSONResponse(
            content={
                "documents": [],
            }
        )


## Search for documentation
@app.post("/api/search_documents")
async def search_documents(payload: QueryPayload):
    try:
        documents = agikb_engine.search_documents(payload.query)
        return JSONResponse(
            content={
                "documents": documents,
            }
        )
    except Exception as e:
        msg.fail(f"All Document retrieval failed: {str(e)}")
        return JSONResponse(
            content={
                "documents": [],
            }
        )
