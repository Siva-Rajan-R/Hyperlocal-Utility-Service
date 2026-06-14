import os
import io
from minio import Minio
from minio.error import S3Error
from icecream import ic
from core.configs.settings_config import SETTINGS

# Initialize MinIO client
MINIO_ENDPOINT = getattr(SETTINGS, "MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = getattr(SETTINGS, "MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = getattr(SETTINGS, "MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = getattr(SETTINGS, "MINIO_SECURE", True)

try:
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )
except Exception as e:
    ic(f"Error initializing MinIO client: {e}")
    minio_client = None

BUCKET_NAME = "hyperlocalassets"

def ensure_bucket_exists():
    if minio_client is None:
        return
    try:
        found = minio_client.bucket_exists(BUCKET_NAME)
        if not found:
            minio_client.make_bucket(BUCKET_NAME)
            ic(f"Created bucket {BUCKET_NAME}")
            
            # Set bucket policy to public read
            policy = f'''{{
                "Version": "2012-10-17",
                "Statement": [
                    {{
                        "Action": [
                            "s3:GetObject"
                        ],
                        "Effect": "Allow",
                        "Principal": {{"AWS": ["*"]}},
                        "Resource": [
                            "arn:aws:s3:::{BUCKET_NAME}/*"
                        ]
                    }}
                ]
            }}'''
            minio_client.set_bucket_policy(BUCKET_NAME, policy)
        else:
            ic(f"Bucket {BUCKET_NAME} already exists")
    except S3Error as err:
        ic(f"Error checking/creating bucket: {err}")

# Try to ensure bucket exists on startup
ensure_bucket_exists()

def upload_file_to_minio(file_bytes: bytes, file_name: str, content_type: str) -> str:
    """
    Uploads a file to MinIO and returns the public URL.
    """
    if minio_client is None:
        raise Exception("MinIO client not configured")
        
    try:
        file_stream = io.BytesIO(file_bytes)
        file_size = len(file_bytes)
        
        minio_client.put_object(
            BUCKET_NAME,
            file_name,
            file_stream,
            file_size,
            content_type=content_type
        )
        
        # Determine the protocol based on secure flag
        protocol = "https" if MINIO_SECURE else "http"
        return f"{protocol}://{MINIO_ENDPOINT}/{BUCKET_NAME}/{file_name}"
        
    except S3Error as err:
        ic(f"Failed to upload to MinIO: {err}")
        raise err

def delete_file_from_minio(file_name: str) -> bool:
    """
    Deletes a file from MinIO.
    """
    if minio_client is None:
        return False
        
    try:
        minio_client.remove_object(BUCKET_NAME, file_name)
        return True
    except S3Error as err:
        ic(f"Failed to delete from MinIO: {err}")
        return False
