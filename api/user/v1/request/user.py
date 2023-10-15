from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    # email: str | None = Field(None, description="Email")
    email: Optional[str] = Field(None, description="Email")
    password: str = Field(..., description="Password")

class ForgotPasswordRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email")

class VerificationCodeRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email")
    code: str = Field(..., description="Code for email verification")
    token: str = Field(..., description="Verification token")

class SendVerificationCodeRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email")