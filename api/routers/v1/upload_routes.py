from fastapi import APIRouter, UploadFile, File, HTTPException,Query
from typing import List
from icecream import ic
from integrations.minio_client import upload_file_to_minio
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict, BaseResponseTypDict, ErrorResponseTypDict
from core.services.upload_service import upload_assets,delete_assets
from core.constants import MAX_FILE_SIZE,ALLOWED_EXTENSIONS
from core.utils.filename_generator import generate_unq_filename
from pydantic import BaseModel


router = APIRouter(
    tags=['Uploads'],
    prefix="/upload"
)

@router.post('/assets')
async def upload_images(files: List[UploadFile] = File(...)):
    if len(files) > 4:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Upload Error",
                description="Maximum of 4 images allowed per upload.",
                success=False,
                status_code=400
            )
        )
        
    uploaded_urls = []
    
    for file in files:
        if file.content_type not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Upload Error",
                    description=f"File type {file.content_type} not allowed. Only JPEG, PNG, and WebP are supported.",
                    success=False,
                    status_code=400
                )
            )
            
        file_bytes = await file.read()
        
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Upload Error",
                    description=f"File {file.filename} exceeds the maximum size of 5MB.",
                    success=False,
                    status_code=400
                )
            )
            
        # Generate a unique filename using UUID and original extension
        ext = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = generate_unq_filename(extenstion=ext)
        
        try:
            url = upload_assets(
                file_data=file_bytes,
                bucket_name="inventoryassets",
                file_name=unique_filename,
                content_type=file.content_type
            )

            uploaded_urls.append(url)

        except Exception as e:
            ic(f"Error uploading file {file.filename}: {e}")
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseTypDict(
                    msg="Upload Error",
                    description="Failed to upload one or more files to storage.",
                    success=False,
                    status_code=500
                )
            )
            
    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Images uploaded successfully",
            status_code=200,
            success=True
        ),
        data=uploaded_urls
    )


# class DeleteAssetsSchema(BaseModel):
#     urls: List[str]

@router.delete('/assets')
async def delete_image(urls:List[str]=Query(...)):
    # Extract filename from url
    try:
        filenames = []
        for url in urls:
            filenames.append(url.split('/')[-1])
        ic(filenames)
        bucket_name=urls[0].split('/')[3]
        ic(bucket_name)
        success = delete_assets(file_names=filenames,bucket_name=bucket_name)
        
        if success:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Image deleted successfully",
                    status_code=200,
                    success=True
                )
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to delete image")
    except Exception as e:
        ic(f"Error deleting image: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete image")
