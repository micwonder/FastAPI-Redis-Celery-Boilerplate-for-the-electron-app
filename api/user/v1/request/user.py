from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str | None = Field(None, description="Email")
    password: str = Field(..., description="Password")

class ForgotPasswordRequest(BaseModel):
    email: str | None = Field(None, description="Email")

class VerificationCodeRequest(BaseModel):
    email: str | None = Field(None, description="Email")
    code: str = Field(..., description="Code for email verification")
    token: str = Field(..., description="Verification token")

class SendVerificationCodeRequest(BaseModel):
    email: str | None = Field(None, description="Email")