from .data_model import UploadUrlRequest
from ..security.api_key_check import read_secret, verify_internal_key

import os, uuid
from datetime import timedelta
from pathlib import Path
from fastapi import Header
from fastapi import APIRouter

from minio import Minio
from minio.error import S3Error

MINIO_ACCESS_KEY = read_secret("minio_app_user")
MINIO_SECRET_KEY = read_secret("minio_app_password")
MINIO_BUCKET = os.environ["MINIO_BUCKET"]
MINIO_ENDPOINT = "minio:9000"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

router = APIRouter()

# --------------------------------------------------
# Generate presigned upload URL
# --------------------------------------------------

@router.post("/api/uploads")
def create_upload_url(
    file: UploadUrlRequest,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    # Generate a unique object name.
    #
    # Example:
    #
    # uploads/550e8400-e29b-41d4-a716-446655440000.pdf

    extension = ""

    if "." in file.filename:
        extension = "." + file.filename.split(".")[-1]

    object_name = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    try:
        url = minio_client.presigned_put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            expires=timedelta(days=1),
        )

        return {
            "object_name": object_name,
            "url": url,
        }

    except S3Error as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# --------------------------------------------------
# Generate download URL
# --------------------------------------------------

@router.get("/api/downloads/{object_name:path}")
def create_download_url(
    object_name: str,
):

    try:

        url = minio_client.presigned_get_object(
            MINIO_BUCKET,
            object_name,
            expires=timedelta(minutes=10),
        )

        return {
            "url": url,
        }

    except S3Error as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

