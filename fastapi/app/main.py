from .security.api_key_check import verify_internal_key
from .routers.minio import router as minio_router
from .routers.run_process import SystemRequest
from .routers.query_route import query_api
from .routers.system_route import system_api

import json
from pathlib import Path
from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(minio_router)
app.include_router(query_api())
app.include_router(system_api())

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)

    return {
        "message": "Hello from FastAPI"
    }

@app.get("/api/index")
async def get_aql_readme(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    filename = "README"
    input_file = str(Path.cwd() /  f"{filename}.md")
    output_file = str(Path.cwd() /  f"{filename}.html")
    await SystemRequest().run_markdown_conversion(input_file, output_file)
    with open(output_file, "r") as f:
        html = f.read()
    return HTMLResponse(content=html)

