from minio import Minio
from ..configs.settings_config import SETTINGS
from icecream import ic
import os,io,json
from typing import Optional,List,Literal
from minio.deleteobjects import DeleteObject


try:
    minio_client=Minio(
        endpoint=SETTINGS.MINIO_ENDPOINT,
        access_key=SETTINGS.MINIO_ACCESS_KEY,
        secret_key=SETTINGS.MINIO_SECRET_KEY,
        secure=SETTINGS.MINIO_SECURE
    )
    ic("Minio Initiallized successfully")

except Exception as e:
    ic("Error initializig the minio client",e)

def create_bucket_with_policy(bucket_name:str,access_type:Literal['Allow','Deny'],actions:List[Literal['delete','write','get']],version:Optional[str]="2012-10-17"):
    actions_mapper={
        "get":"s3:GetObject",
        "write":"s3:PutObject",
        "delete":"s3:DeleteObject"
    }
    if not minio_client.bucket_exists(bucket_name=bucket_name):
        minio_client.make_bucket(bucket_name)
        ic(f"Created MinIO Bucket: {bucket_name}")
    policy_actions=[]
    for action in actions:
        policy_actions.append(actions_mapper[action])
    
    ic(policy_actions)
            
    policy = {
        "Version": version,
        "Statement": [
            {
                "Sid": "PublicReadPutDelete",
                "Effect": access_type,
                "Principal": "*",
                "Action": policy_actions,
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
            }
        ],
    }
    ic(json.dumps(policy, indent=2))
    minio_client.set_bucket_policy(bucket_name, json.dumps(policy))
    ic(minio_client.get_bucket_policy(bucket_name=bucket_name))

    return True

    

def upload_assets(file_data,bucket_name: str,file_name:str,content_type:str):
    if not minio_client:
        ic("MinIO client is not initialized")
    
    try:
        res=create_bucket_with_policy(
            bucket_name=bucket_name,
            access_type="Allow",
            actions=["get"]
        )
        ic(res)

        file_len=len(file_data)
        stream=io.BytesIO(file_data)
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=stream,
            length=file_len,
            content_type=content_type
        )


        protocol="https" if SETTINGS.MINIO_SECURE else "http"
        asset_url=f"{protocol}://{SETTINGS.MINIO_ENDPOINT}/{bucket_name}/{file_name}"
        ic(asset_url)
        return asset_url
    
    except Exception as e:
        ic(f"MinIO unexpected error during upload: {e}")
        raise RuntimeError(f"Storage upload failed: {e}")

  
def delete_assets(bucket_name:str,file_names: List[str]):
    if not file_names:
        return True

    if minio_client is None:
        return False
    
    objects=[DeleteObject(obj) for obj in file_names]

    responses=minio_client.remove_objects(
        bucket_name=bucket_name,
        delete_object_list=objects
    )
    ic(list(responses))
    return responses
