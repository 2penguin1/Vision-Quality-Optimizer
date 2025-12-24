from bson import ObjectId
from app.models.db_models import Comparison
from typing import Optional, List


class ComparisonService:
    """Service for image comparison operations"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.comparisons
    
    async def create_comparison(self, user_id: str, image1_id: str, image2_id: str, 
                               quality_metrics: dict, enhancements: dict, 
                               enhanced_image_s3_url: Optional[str] = None,
                               processing_time: float = 0.0) -> dict:
        """Save comparison result"""
        comparison = Comparison(
            user_id=user_id,
            image1_id=image1_id,
            image2_id=image2_id,
            quality_metrics=quality_metrics,
            enhancements=enhancements,
            enhanced_image_s3_url=enhanced_image_s3_url,
            processing_time=processing_time
        )
        result = await self.collection.insert_one(comparison.to_dict())
        
        return {
            "id": str(result.inserted_id),
            "user_id": user_id,
            "image1_id": image1_id,
            "image2_id": image2_id,
            "quality_metrics": quality_metrics,
            "enhancements": enhancements,
            "enhanced_image_s3_url": enhanced_image_s3_url,
            "processing_time": processing_time
        }
    
    async def get_comparison(self, comparison_id: str) -> Optional[dict]:
        """Get comparison by ID"""
        return await self.collection.find_one({"_id": ObjectId(comparison_id)})
    
    async def get_user_comparisons(self, user_id: str, limit: int = 50, skip: int = 0) -> List[dict]:
        """Get all comparisons for a user"""
        cursor = self.collection.find({"user_id": user_id}).skip(skip).limit(limit).sort("created_at", -1)
        return await cursor.to_list(length=limit)
    
    async def delete_comparison(self, comparison_id: str, user_id: str) -> bool:
        """Delete a comparison"""
        result = await self.collection.delete_one({"_id": ObjectId(comparison_id), "user_id": user_id})
        return result.deleted_count > 0
