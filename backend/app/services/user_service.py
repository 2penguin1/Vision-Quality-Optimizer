from bson import ObjectId
from app.models.db_models import User
from app.core.security import hash_password, verify_password
from typing import Optional


class UserService:
    """Service for user operations"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.users
    
    async def create_user(self, email: str, name: str, password: str) -> dict:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        hashed_password = hash_password(password)
        user = User(email=email, name=name, hashed_password=hashed_password)
        
        result = await self.collection.insert_one(user.to_dict())
        return {"id": str(result.inserted_id), "email": email, "name": name}
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        return await self.collection.find_one({"email": email})
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        return await self.collection.find_one({"_id": ObjectId(user_id)})
    
    async def verify_user_password(self, email: str, password: str) -> Optional[dict]:
        """Verify user credentials"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        
        if verify_password(password, user["hashed_password"]):
            return user
        return None
    
    async def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user information"""
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": kwargs}
        )
        return result.modified_count > 0
