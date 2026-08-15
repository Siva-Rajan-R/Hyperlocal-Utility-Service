import asyncio
from minio import Minio
import json
import io

minio_client = Minio(
    endpoint="localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "inventoryassets"

try:
    if not minio_client.bucket_exists(bucket_name):
        print("Making bucket...")
        minio_client.make_bucket(bucket_name)
    print("Bucket exists.")
    
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadPutDelete",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
            }
        ],
    }
    print("Setting bucket policy...")
    minio_client.set_bucket_policy(bucket_name, json.dumps(policy))
    print("Policy set.")
    
    print("Putting object...")
    stream = io.BytesIO(b"test")
    minio_client.put_object(
        bucket_name=bucket_name,
        object_name="test.txt",
        data=stream,
        length=4,
        content_type="text/plain"
    )
    print("Object put.")
except Exception as e:
    print(f"Error: {e}")
