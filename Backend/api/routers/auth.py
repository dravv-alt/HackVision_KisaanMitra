"""
Authentication API Router
Handles phone-based OTP authentication using Twilio
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from Backend.auth.twilio_service import get_twilio_service
from Backend.auth.jwt_service import get_jwt_service
from Backend.api.dependencies import get_db_client

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Request/Response Models
class SendOTPRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 format (e.g., +919876543210)")

class SendOTPResponse(BaseModel):
    success: bool
    message: str
    expires_in_minutes: Optional[int] = None
    status: Optional[str] = None
    otp: Optional[str] = None  # Only in mock mode

class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 format")
    otp: str = Field(..., description="6-digit OTP")
    name: Optional[str] = Field(None, description="User's name (for new users)")

class VerifyOTPResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str] = None
    user_id: Optional[str] = None
    farmer_id: Optional[str] = None
    is_new_user: bool = False
    needs_onboarding: bool = False

class RefreshTokenResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    message: Optional[str] = None

# API Endpoints

@router.post("/send-otp", response_model=SendOTPResponse)
async def send_otp(request: SendOTPRequest):
    """
    Send OTP to phone number via SMS
    
    - **phone_number**: Phone number in E.164 format (e.g., +919876543210)
    """
    twilio_service = get_twilio_service()
    result = twilio_service.send_otp(request.phone_number)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return SendOTPResponse(**result)

@router.post("/verify-otp", response_model=VerifyOTPResponse)
async def verify_otp(
    request: VerifyOTPRequest,
    db_client = Depends(get_db_client)
):
    """
    Verify OTP and authenticate user
    
    - **phone_number**: Phone number
    - **otp**: 6-digit OTP received via SMS
    - **name**: User's name (optional, for new users)
    
    Returns JWT access token on successful verification
    """
    twilio_service = get_twilio_service()
    jwt_service = get_jwt_service()
    
    # Verify OTP
    verification_result = twilio_service.verify_otp(request.phone_number, request.otp)
    
    if not verification_result["success"]:
        raise HTTPException(status_code=400, detail=verification_result["message"])
    
    # OTP verified - check if user exists in database
    db = db_client["kisanmitra"]
    user = db.farmers.find_one({"phone": request.phone_number})
    
    is_new_user = user is None
    needs_onboarding = False
    
    if is_new_user:
        # Create new user
        import uuid
        user_id = f"U{str(uuid.uuid4())[:8].upper()}"
        farmer_id = f"F{str(uuid.uuid4())[:8].upper()}"
        
        new_user = {
            "user_id": user_id,
            "farmer_id": farmer_id,
            "phone": request.phone_number,
            "name": request.name or "Farmer",
            "language": "hi",  # Default to Hindi
            "onboarding_completed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        db.farmers.insert_one(new_user)
        needs_onboarding = True
    else:
        user_id = user.get("user_id")
        farmer_id = user.get("farmer_id")
        needs_onboarding = not user.get("onboarding_completed", False)
    
    # Generate JWT token
    token_data = {
        "user_id": user_id,
        "farmer_id": farmer_id,
        "phone_number": request.phone_number
    }
    
    access_token = jwt_service.create_access_token(token_data)
    
    return VerifyOTPResponse(
        success=True,
        message="Authentication successful",
        access_token=access_token,
        user_id=user_id,
        farmer_id=farmer_id,
        is_new_user=is_new_user,
        needs_onboarding=needs_onboarding
    )

@router.post("/resend-otp", response_model=SendOTPResponse)
async def resend_otp(request: SendOTPRequest):
    """
    Resend OTP to phone number
    
    - **phone_number**: Phone number in E.164 format
    """
    twilio_service = get_twilio_service()
    result = twilio_service.resend_otp(request.phone_number)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return SendOTPResponse(**result)

@router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(authorization: str = Header(None)):
    """
    Refresh JWT access token
    
    - **Authorization**: Bearer token in header
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    jwt_service = get_jwt_service()
    
    new_token = jwt_service.refresh_token(token)
    
    if not new_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return RefreshTokenResponse(
        success=True,
        access_token=new_token,
        message="Token refreshed successfully"
    )

@router.get("/verify-token")
async def verify_token(authorization: str = Header(None)):
    """
    Verify if JWT token is valid
    
    - **Authorization**: Bearer token in header
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    jwt_service = get_jwt_service()
    
    payload = jwt_service.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "success": True,
        "message": "Token is valid",
        "user_data": payload
    }
