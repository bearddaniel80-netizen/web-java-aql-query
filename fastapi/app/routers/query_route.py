from .data_model import QueryRequest
from .run_process import QueryPullRequest
from ..security.api_key_check import verify_internal_key

import asyncio
from fastapi import Header, APIRouter, HTTPException
import uuid

def query_api():

    query_pull = QueryPullRequest()
    router = APIRouter(prefix="/api/query")

    @router.post("/submit/{query}")
    async def submit_query(
        query: str,
        x_internal_key: str | None = Header(default=None),
    ):
        verify_internal_key(x_internal_key)

        job_id = str(uuid.uuid4())

        query_pull.query_jobs[job_id] = {
            "jobId": job_id,
            "status": "pending",
            "results": [],
            "columns": []
        }

        asyncio.create_task(
            query_pull.execute_query(job_id, query)
        )

        return {
            "jobId": job_id,
            "status": "pending"
        }

    @router.get("/results/{jobId}")
    async def get_query_results(
        jobId: str,
        x_internal_key: str | None = Header(default=None),
    ):
        verify_internal_key(x_internal_key)

        job = query_pull.query_jobs.get(jobId)

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="Query job not found"
            )

        return job

    return router