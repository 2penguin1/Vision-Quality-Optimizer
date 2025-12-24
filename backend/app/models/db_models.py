from bson import ObjectId
from datetime import datetime
from typing import Optional


class User:
    """User model for MongoDB"""
    
    def __init__(self, email: str, name: str, hashed_password: str, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "email": self.email,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict):
        return User(
            email=data.get("email"),
            name=data.get("name"),
            hashed_password=data.get("hashed_password"),
            _id=data.get("_id")
        )


class Image:
    """Image model for MongoDB"""
    
    def __init__(self, user_id: str, name: str, s3_url: str, description: Optional[str] = None, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.s3_url = s3_url
        self.uploaded_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "s3_url": self.s3_url,
            "uploaded_at": self.uploaded_at
        }


class Comparison:
    """Comparison model for MongoDB"""
    
    def __init__(self, user_id: str, image1_id: str, image2_id: str, quality_metrics: dict, 
                 enhancements: dict, enhanced_image_s3_url: Optional[str] = None, 
                 processing_time: float = 0.0, _id: Optional[ObjectId] = None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.image1_id = image1_id
        self.image2_id = image2_id
        self.quality_metrics = quality_metrics
        self.enhancements = enhancements
        self.enhanced_image_s3_url = enhanced_image_s3_url
        self.processing_time = processing_time
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "image1_id": self.image1_id,
            "image2_id": self.image2_id,
            "quality_metrics": self.quality_metrics,
            "enhancements": self.enhancements,
            "enhanced_image_s3_url": self.enhanced_image_s3_url,
            "processing_time": self.processing_time,
            "created_at": self.created_at
        }
