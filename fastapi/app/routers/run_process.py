import asyncio
import subprocess
import json

class QueryPullRequest:
    def __init__(self):
        # Demo storage. Use Redis or a database in production.
        self.query_jobs = {}

    def _get_data_type(self, value):
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        if isinstance(value, str):
            return "string"
        return "unknown"

    def _get_unique_columns(self, output):
        return [
            {
                "key": key,
                "label": key.title(),
                "type": self._get_data_type(value)
            }
            for key, value in output[0].items()
        ]

    async def run_query(self, command):
        result = await asyncio.to_thread(
            subprocess.run,
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr or "Query execution failed"
            )

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid JSON returned by AQL: {exc}"
            )

    async def execute_query(self, job_id, query):
        self.query_jobs[job_id]["status"] = "running"

        try:
            command = ["aql", "query", query]

            output = await self.run_query(command)

            self.query_jobs[job_id].update({
                "status": "completed",
                "results": output,
                "columns": self._get_unique_columns(output)
            })

        except Exception as exc:
            self.query_jobs[job_id].update({
                "status": "failed",
                "error": str(exc)
            })

class SystemRequest:
    async def run_query_to_file(self, command, filename):
        def execute():
            with open(filename, "w+") as log:
                result = subprocess.run(
                    command,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                return result.returncode

        await asyncio.to_thread(execute)

    async def run_markdown_conversion(self, input_file, output_file):
        command = ["pandoc", "-f", "markdown-yaml_metadata_block", input_file, "-o", output_file]
        await self.run_query_to_file(command, output_file)