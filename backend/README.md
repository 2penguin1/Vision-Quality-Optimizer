# Image Quality Optimization - Backend README

## Overview

This is the backend service for the Image Quality Optimization system. It provides:

- **User Authentication**: JWT-based authentication with register/login/refresh
- **Image Management**: Upload, retrieve, and delete images via AWS S3
- **Quality Assessment**: ML-based image quality metrics (sharpness, contrast, noise, color)
- **Image Comparison**: Compare quality metrics between two images
- **Enhancement**: Adaptive image enhancement with user control

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (with Motor async driver)
- **Storage**: AWS S3
- **Authentication**: JWT
- **Image Processing**: OpenCV, PyTorch, TensorFlow.js
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## Installation

### Local Development

1. **Clone the repository**

```bash
cd backend
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your actual values
```

5. **Start MongoDB** (if local)

```bash
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo:7.0
```

6. **Run the server**

```bash
python -m app.main
# Or use: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build Docker image
docker build -t image-quality-backend .

# Run with Docker Compose
docker-compose up -d
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password",
    "name": "John Doe"
  }
  ```

- `POST /auth/login` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```

- `POST /auth/refresh` - Refresh access token
  ```json
  {
    "refresh_token": "token_value"
  }
  ```

### Images

- `POST /images/upload` - Upload image (requires auth)
  - Form data with `file` and optional `description`

- `GET /images/my-images` - Get user's images (requires auth)
  - Query params: `skip`, `limit`

- `GET /images/{image_id}` - Get image details (requires auth)

- `DELETE /images/{image_id}` - Delete image (requires auth)

- `POST /images/compare` - Compare two images (requires auth)
  ```json
  {
    "image1_id": "id1",
    "image2_id": "id2",
    "enhancement_level": 0.5
  }
  ```

### Health

- `GET /health` - Health check endpoint

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── security.py      # JWT and password hashing
│   │   └── database.py      # MongoDB connection
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── images.py        # Image endpoints
│   ├── services/
│   │   ├── user_service.py
│   │   ├── image_service.py
│   │   ├── comparison_service.py
│   │   └── s3_service.py
│   ├── models/
│   │   └── db_models.py     # Database models
│   ├── schemas/
│   │   ├── user.py          # User request/response schemas
│   │   └── image.py         # Image request/response schemas
│   ├── ml/
│   │   └── pipeline.py      # ML model placeholder
│   └── main.py              # FastAPI application
├── config/
│   ├── settings.py          # Configuration
│   └── __init__.py
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── Dockerfile              # Docker build config
└── docker-compose.yml      # Docker Compose config
```

## Configuration

### Environment Variables

```
# API
DEBUG=True
API_TITLE="Image Quality Optimization API"
API_VERSION="1.0.0"

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=image_quality

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=bucket-name
AWS_REGION=us-east-1

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

## Database Schema

### Users Collection

```javascript
{
  _id: ObjectId,
  email: String (unique),
  name: String,
  hashed_password: String,
  created_at: Date,
  updated_at: Date
}
```

### Images Collection

```javascript
{
  _id: ObjectId,
  user_id: String,
  name: String,
  description: String,
  s3_url: String,
  uploaded_at: Date
}
```

### Comparisons Collection

```javascript
{
  _id: ObjectId,
  user_id: String,
  image1_id: String,
  image2_id: String,
  quality_metrics: Object,
  enhancements: Object,
  enhanced_image_s3_url: String,
  processing_time: Float,
  created_at: Date
}
```

## ML Pipeline

The `app/ml/pipeline.py` provides the backbone for:

1. **Quality Assessment** - Evaluates images for:
   - Sharpness
   - Contrast
   - Noise levels
   - Color accuracy

2. **Enhancement Algorithm** - Applies targeted improvements based on:
   - Quality metric differences
   - User enhancement level (0-1)
   - Specific quality aspects

### Current Implementation

Currently uses placeholder implementations. To implement actual ML models:

1. Train/download BRISQUE, NIQE models for quality assessment
2. Implement enhancement using OpenCV filters or deep learning
3. Integrate pretrained models into the pipeline
4. Update requirements.txt with ML library versions

## Testing

Run tests with pytest:

```bash
pip install pytest pytest-asyncio
pytest
```

## Performance Metrics (KPI)

- **Quality Metric Accuracy**: ≥ 90%
- **Processing Time**: ≤ 2s per image pair
- **PSNR Improvement**: ≥ 25%
- **User Satisfaction**: ≥ 85%

## Security Considerations

1. **JWT Tokens**
   - Access tokens: 30 minutes expiry
   - Refresh tokens: 7 days expiry
   - Always use HTTPS in production

2. **Password Security**
   - BCrypt hashing with cost factor
   - Minimum 8 characters required

3. **AWS S3**
   - Use IAM roles instead of access keys
   - Enable bucket encryption
   - Set appropriate CORS headers

4. **CORS**
   - Currently allows all origins (update in production)
   - Configure for specific domains

## Deployment

See `config/EC2_DEPLOYMENT.md` for detailed EC2 deployment guide.

### Quick Docker Deployment

```bash
# Create .env file with production values
cp .env.example .env

# Start with Docker Compose
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f backend
```

## Development Tips

1. **Debug Mode**: Set `DEBUG=True` in .env for detailed error messages
2. **Async Operations**: Use `async/await` consistently
3. **Error Handling**: All routes should return appropriate HTTP status codes
4. **Logging**: Use Python's logging module for production debugging
5. **Testing**: Write tests for all business logic

## Future Enhancements

- [ ] Implement actual ML models for quality assessment
- [ ] Add batch image processing
- [ ] WebSocket support for real-time comparison feedback
- [ ] Image enhancement preview before saving
- [ ] Multi-language support
- [ ] Advanced filtering and search
- [ ] User analytics dashboard

## Support and Contribution

For issues and contributions, please refer to the main project documentation.
