from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from app.db.models import User as UserModel
import structlog

logger = structlog.get_logger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        existing = await UserModel.find_first(where={"email": user.email})
        if existing:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        new_user = await UserModel.create(
            email=user.email,
            fullName=user.name,
            hashedPassword=pwd_context.hash(user.password),
        )
        return UserResponse(id=new_user.id, email=new_user.email, name=new_user.fullName or user.name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("User creation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user information"""
    try:
        user = await UserModel.find_first(where={"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=user.id, email=user.email, name=user.fullName or "")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("User retrieval failed", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve user")