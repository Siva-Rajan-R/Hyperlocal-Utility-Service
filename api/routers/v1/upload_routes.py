from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from icecream import ic
from integrations.minio_client import upload_file_to_minio
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict, BaseResponseTypDict, ErrorResponseTypDict

router = APIRouter(
    tags=['Uploads'],
    prefix="/upload"
)

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@router.post('/images')
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
        unique_filename = f"{generate_uuid()}.{ext}" if ext else generate_uuid()
        
        try:
            url = upload_file_to_minio(file_bytes, unique_filename, file.content_type)
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

@router.delete('/images')
async def delete_image(url: str):
    from integrations.minio_client import delete_file_from_minio
    # Extract filename from url
    try:
        filename = url.split('/')[-1]
        success = delete_file_from_minio(filename)
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
