import os
from pathlib import Path
from fastapi import HTTPException


def read_secret(name: str) -> str:
    path = f"/run/secrets/{name}"

    if os.path.exists(path):
        return Path(path).read_text().strip()

    # Useful for local development outside Docker
    return os.environ[name]

INTERNAL_API_KEY = read_secret("fastapi_internal_key")

def verify_internal_key(
    x_internal_key: str | None,
):
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )