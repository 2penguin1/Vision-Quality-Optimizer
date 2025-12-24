import boto3
from botocore.exceptions import ClientError
from config.settings import settings
from io import BytesIO
import mimetypes


class S3Service:
    """AWS S3 service for image storage"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_S3_BUCKET
    
    async def upload_image(self, file_content: bytes, file_name: str, user_id: str) -> dict:
        """
        Upload image to S3
        Returns: {"url": "s3_url", "key": "object_key"}
        """
        try:
            # Generate object key
            object_key = f"uploads/{user_id}/{file_name}"
            
            # Get content type
            content_type, _ = mimetypes.guess_type(file_name)
            if not content_type:
                content_type = "image/jpeg"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{object_key}"
            
            return {"url": url, "key": object_key}
        except ClientError as e:
            raise Exception(f"Error uploading to S3: {str(e)}")
    
    async def delete_image(self, object_key: str) -> bool:
        """Delete image from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError as e:
            raise Exception(f"Error deleting from S3: {str(e)}")
    
    async def download_image(self, object_key: str) -> bytes:
        """Download image from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            return response["Body"].read()
        except ClientError as e:
            raise Exception(f"Error downloading from S3: {str(e)}")
    
    async def generate_presigned_url(self, object_key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for direct access"""
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise Exception(f"Error generating presigned URL: {str(e)}")


# Singleton instance
s3_service = S3Service()
