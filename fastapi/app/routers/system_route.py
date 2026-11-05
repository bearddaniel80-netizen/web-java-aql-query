from .run_process import SystemRequest
from ..security.api_key_check import verify_internal_key

import json
from fastapi import Header, APIRouter
from pathlib import Path

def system_api():

    system = SystemRequest()
    router = APIRouter(prefix="/api/system")

    @router.get("/list")
    async def get_system_list(
        x_internal_key: str | None = Header(default=None),
    ):
        verify_internal_key(x_internal_key)
        return {"result": ["aggregates", "docs", "docs_filter", "operators", "scalars", "stdin_sources","table_functions","transformers"]}

    @router.get("/fields/{source}")
    async def get_system_source_fields(
        source: str,
        x_internal_key: str | None = Header(default=None),
    ):
        verify_internal_key(x_internal_key)

        # --------- Data files ------------
        metadata_filename = str(Path.cwd() / f"{source}_metadata.js")

        # --------- Run command -----------
        command = ["aql", "query", f"DESCRIBE {source}"]
        await system.run_query_to_file(command, metadata_filename)

        # --------- Collect / Format ------
        with open(metadata_filename, "r") as f_metadata:
            tmp_columns = json.load(f_metadata)
            columns = [
                column["name"] for column in tmp_columns 
            ]
        return {"fields": columns}

    @router.get("/{source}")
    async def get_system_source(
        source: str,
        x_internal_key: str | None = Header(default=None),
    ):
        verify_internal_key(x_internal_key)

        # --------- Data files ------------
        data_filename = str(Path.cwd() / f"{source}_data.js")
        metadata_filename = str(Path.cwd() / f"{source}_metadata.js")

        # --------- Run command -----------
        command = ["aql", "query", f"SHOW {source}"]
        await system.run_query_to_file(command, data_filename)
        command = ["aql", "query", f"DESCRIBE {source}"]
        await system.run_query_to_file(command, metadata_filename)

        # --------- Collect / Format ------
        with open(data_filename, "r") as f_data:
            data = json.load(f_data)
        with open(metadata_filename, "r") as f_metadata:
            tmp_columns = json.load(f_metadata)
            columns = [
                {
                    "key": column["name"],
                    "label": column["name"].title(),
                    "type": column["type"]
                }
                for column in tmp_columns 
            ]
        return {"columns": columns, "results": data}

    return router