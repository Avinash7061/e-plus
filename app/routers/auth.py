from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from app.core.supabase_client import get_supabase
from app.schemas.user import RegisterRequest, LoginRequest
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(request: RegisterRequest, db: Client = Depends(get_supabase)):
    """Registers a new user, returning an access token and user profile"""
    existing = db.table("users").select("id").eq("phone_number", request.phone_number).execute()
    if existing.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
    
    new_user_data = {
        "phone_number": request.phone_number,
        "full_name": request.full_name,
        "role": request.role
    }
    response = db.table("users").insert(new_user_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
        
    user = response.data[0]
    access_token = create_access_token(user_id=user["id"])
    
    return {"access_token": access_token, "user": user}

@router.post("/login")
def login(request: LoginRequest, db: Client = Depends(get_supabase)):
    """Logs in an existing user via phone number, returning an access token and user profile"""
    response = db.table("users").select("*").eq("phone_number", request.phone_number).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    user = response.data[0]
    access_token = create_access_token(user_id=user["id"])
    
    return {"access_token": access_token, "user": user}
