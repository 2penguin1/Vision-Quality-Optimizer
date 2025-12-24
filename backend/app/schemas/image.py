from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageUpload(BaseModel):
    """Image upload schema"""
    name: str
    description: Optional[str] = None


class ImageResponse(BaseModel):
    """Image response schema"""
    id: str
    user_id: str
    name: str
    description: Optional[str]
    s3_url: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class ComparisonRequest(BaseModel):
    """Image comparison request schema"""
    image1_id: str
    image2_id: str
    enhancement_level: Optional[float] = 0.5  # 0.0 to 1.0
    
    class Config:
        json_schema_extra = {
            "example": {
                "image1_id": "image_id_1",
                "image2_id": "image_id_2",
                "enhancement_level": 0.7
            }
        }


class ComparisonResult(BaseModel):
    """Comparison result schema"""
    comparison_id: str
    image1_id: str
    image2_id: str
    quality_metrics: dict
    enhancements: dict
    enhanced_image_s3_url: Optional[str]
    processing_time: float
    created_at: datetime
    
    class Config:
        from_attributes = True
