from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Header, Query
from app.services.image_service import ImageService
from app.services.s3_service import s3_service
from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.image import ComparisonRequest, ComparisonResult
from app.services.comparison_service import ComparisonService
from app.ml.pipeline import ml_pipeline
from typing import Optional
import cv2
import numpy as np
from io import BytesIO

router = APIRouter(prefix="/images", tags=["Images"])


async def get_current_user(authorization: str = Header()):
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
    
    token = authorization[7:]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return payload.get("sub")


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    description: Optional[str] = None,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Upload an image to S3 and save metadata"""
    try:
        # Read file
        file_content = await file.read()
        
        # Validate image
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")
        
        # Upload to S3
        s3_result = await s3_service.upload_image(file_content, file.filename, current_user)
        
        # Save metadata to MongoDB
        image_service = ImageService(db)
        image_record = await image_service.upload_image(
            user_id=current_user,
            name=file.filename,
            s3_url=s3_result["url"],
            description=description
        )
        
        return {
            "message": "Image uploaded successfully",
            "image": image_record
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/my-images")
async def get_user_images(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get all images for current user"""
    try:
        image_service = ImageService(db)
        images = await image_service.get_user_images(current_user, limit=limit, skip=skip)
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{image_id}")
async def get_image(
    image_id: str,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get image details"""
    try:
        image_service = ImageService(db)
        image = await image_service.get_image(image_id)
        
        if not image or image["user_id"] != current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        
        return image
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Delete an image"""
    try:
        image_service = ImageService(db)
        image = await image_service.get_image(image_id)
        
        if not image or image["user_id"] != current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        
        # Delete from S3
        # Extract key from S3 URL
        s3_key = image["s3_url"].split(f"{image['user_id']}/")[1]
        await s3_service.delete_image(f"uploads/{current_user}/{s3_key}")
        
        # Delete from MongoDB
        await image_service.delete_image(image_id, current_user)
        
        return {"message": "Image deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/compare")
async def compare_images(
    request: ComparisonRequest,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Compare two images and generate quality metrics and enhancements
    """
    try:
        image_service = ImageService(db)
        comparison_service = ComparisonService(db)
        
        # Verify both images belong to user
        image1 = await image_service.get_image(request.image1_id)
        image2 = await image_service.get_image(request.image2_id)
        
        if not image1 or image1["user_id"] != current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image 1 not found")
        if not image2 or image2["user_id"] != current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image 2 not found")
        
        # Download images from S3
        # Extract S3 keys
        key1 = image1["s3_url"].split(f"/{current_user}/")[1]
        key2 = image2["s3_url"].split(f"/{current_user}/")[1]
        
        img1_bytes = await s3_service.download_image(f"uploads/{current_user}/{key1}")
        img2_bytes = await s3_service.download_image(f"uploads/{current_user}/{key2}")
        
        # Convert to numpy arrays
        nparr1 = np.frombuffer(img1_bytes, np.uint8)
        nparr2 = np.frombuffer(img2_bytes, np.uint8)
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
        
        # Process through ML pipeline
        result = await ml_pipeline.process_images(img1, img2, request.enhancement_level)
        
        # Save comparison to database
        comparison = await comparison_service.create_comparison(
            user_id=current_user,
            image1_id=request.image1_id,
            image2_id=request.image2_id,
            quality_metrics=result["quality_metrics"],
            enhancements=result["enhancements"],
            processing_time=result["processing_time"]
        )
        
        return comparison
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
