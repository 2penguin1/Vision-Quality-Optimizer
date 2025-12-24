from bson import ObjectId
from app.models.db_models import Image
from typing import Optional, List


class ImageService:
    """Service for image operations"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.images
    
    async def upload_image(self, user_id: str, name: str, s3_url: str, description: Optional[str] = None) -> dict:
        """Save image metadata to database"""
        image = Image(user_id=user_id, name=name, s3_url=s3_url, description=description)
        result = await self.collection.insert_one(image.to_dict())
        
        return {
            "id": str(result.inserted_id),
            "user_id": user_id,
            "name": name,
            "s3_url": s3_url,
            "description": description
        }
    
    async def get_image(self, image_id: str) -> Optional[dict]:
        """Get image by ID"""
        return await self.collection.find_one({"_id": ObjectId(image_id)})
    
    async def get_user_images(self, user_id: str, limit: int = 50, skip: int = 0) -> List[dict]:
        """Get all images for a user"""
        cursor = self.collection.find({"user_id": user_id}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def delete_image(self, image_id: str, user_id: str) -> bool:
        """Delete an image"""
        result = await self.collection.delete_one({"_id": ObjectId(image_id), "user_id": user_id})
        return result.deleted_count > 0
    
    async def update_image(self, image_id: str, user_id: str, **kwargs) -> bool:
        """Update image metadata"""
        result = await self.collection.update_one(
            {"_id": ObjectId(image_id), "user_id": user_id},
            {"$set": kwargs}
        )
        return result.modified_count > 0
