import math
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Header, Request

from api.user.v1.request.user import (
    ForgotPasswordRequest,
    LoginRequest,
    SendVerificationCodeRequest,
    VerificationCodeRequest,
)

from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
)
from app.user.schemas import ChangePasswordRequestSchema, ResetPasswordRequestSchema, UpdateUserRequestSchema
from app.user.services import UserService
from core.exceptions.base import ForbiddenException
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
    IsAuthenticated,
)
from core.utils import TokenHelper
from utils.util_datetime import now

user_router = APIRouter()

############### get user list ###############
@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    #response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
    page: int = Query(0, description="Page Number"),    
    size: int = Query(10, description="Size"),
    order_by: str = Query("name", description="Sort by spec field"),
    desc: bool = Query(False, description="Descending order"),
):
    return await UserService().get_user_list(page=page, size=size, order_by=order_by, desc=desc)

############### create user ###############
@user_router.post(
    "/register",
    response_model=None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(body: CreateUserRequestSchema):
    ts = now()
    response = await UserService().create_user(**body.dict())
    consumed = math.ceil((now().timestamp()-ts.timestamp())*1000)
    response["consumed"] = f"Finished in {consumed}ms"

    return response

############### update user ###############
@user_router.put(
    "/update",
    response_model=None,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def update_user(
    request: Request,
    body: UpdateUserRequestSchema,
):
    return await UserService().update_user(**body.dict(), user_id=request.user.id)

############### login ###############
@user_router.post(
    "/login",
    response_model=None,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def login(body: LoginRequest):
    ts = now()
    response = await UserService().login(**body.dict())
    consumed = math.ceil((now().timestamp()-ts.timestamp())*1000)
    response["consumed"] = f"Finished in {consumed}ms"
    
    return response

############### forgot password ###############
@user_router.post(
    "/forgot-password",
    response_model=None,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def forgot_password(body: ForgotPasswordRequest):
    ts = now()
    response = await UserService().forgot_password(**body.dict())
    consumed = math.ceil((now().timestamp()-ts.timestamp())*1000)
    response["consumed"] = f"Finished in {consumed}ms"

    return response

############### reset password ###############
@user_router.post(
    "/reset-password",
    response_model=None,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def reset_password(request: ResetPasswordRequestSchema):
    return await UserService().reset_password(**request.dict())

############### change password ###############
@user_router.put(
    "/change-password",
    response_model=None,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def change_password(
    request: Request,
    body: ChangePasswordRequestSchema,
):
    return await UserService().change_password(user_id=request.user.id, **body.dict())

############### delete ###############
@user_router.delete(
    "/delete",
    response_model=None,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def delete(request: Request):
    return await UserService().delete(user_id=request.user.id)