from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
from app.schemas.user import UserRegister, UserLogin, TokenResponse, RefreshTokenRequest
from app.services.user_service import UserService
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from datetime import timedelta
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db=Depends(get_db)):
    """Register a new user"""
    try:
        user_service = UserService(db)
        user = await user_service.create_user(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        
        # Generate tokens
        access_token = create_access_token({"sub": user["id"], "email": user_data.email})
        refresh_token = create_refresh_token({"sub": user["id"], "email": user_data.email})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db=Depends(get_db)):
    """Login user"""
    try:
        user_service = UserService(db)
        user = await user_service.verify_user_password(credentials.email, credentials.password)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
        refresh_token = create_refresh_token({"sub": str(user["_id"]), "email": user["email"]})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        payload = verify_token(request.refresh_token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        # Generate new access token
        access_token = create_access_token({"sub": payload["sub"], "email": payload.get("email")})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
