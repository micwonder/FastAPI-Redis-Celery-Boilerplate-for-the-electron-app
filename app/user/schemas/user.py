from pydantic import BaseModel, Field
from typing import Optional

class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: Optional[str] = Field(None, description="Email")
    name: str = Field(..., description="Name")
    user_type: str = Field(..., description="User type")
    class Config:
        orm_mode = True

class CreateUserRequestSchema(BaseModel):
    email: Optional[str] = Field(None, description="Email")
    password: str = Field(..., description="Password")
    password_confirmation: str = Field(..., description="Password Confirmation")
    name: str = Field(..., description="Name")

class UpdateUserRequestSchema(BaseModel):
    name: Optional[str] = Field(None, description="Name")
    # user_type: str | None = Field(None, description="User type")

class ResetPasswordRequestSchema(BaseModel):
    token: str = Field(..., description="Token")
    new_password1: str = Field(..., description="New Password")
    new_password2: str = Field(..., description="Password Confirmation")

class ChangePasswordRequestSchema(BaseModel):
    password: str = Field(..., description="Password")
    new_password1: str = Field(..., description="New Password")
    new_password2: str = Field(..., description="Password Confirmation")

class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")

class ChangePasswordResponseSchema(BaseModel):
    success: bool = Field(..., description="Success or not")
    message: str = Field(..., description="ChangePassword")