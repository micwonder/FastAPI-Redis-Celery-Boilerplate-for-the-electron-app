import random

import bcrypt

from sqlalchemy import select, func, and_
from app.user.models import User


from app.user.schemas import LoginResponseSchema, ChangePasswordResponseSchema
from core.db import Transactional, session

from core.exceptions import (
    UnprocessableEntity,
    BadRequestException,
    UnauthorizedException,
    DuplicateValueException,
)
from core.utils.token_helper import TokenHelper
from utils.validator import validation, user_availability

from utils.util_datetime import now


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
        self,
        page: int,
        size: int,    # optional[int]
        order_by: str,
        desc: bool,
    ) -> dict:
        try:
            print("~~~~~~~~~~~~~~~~~~~~~~~ get user list request")
            if size > 100:
                size = 100
            offset = page*size
            if desc:
                query = select(User).order_by(getattr(User, order_by).desc())
            else:
                query = select(User).order_by(getattr(User, order_by))
            query = query.where(User.deleted_at == None)
            query = query.offset(offset).limit(size)
            result = await session.execute(query)
            result = result.scalars().all()
            print("get user list success")
            return result
        except:
            raise UnprocessableEntity

    @Transactional()
    async def create_user(
        self,
        name: str,
        email: str,
        password: str,
        password_confirmation: str,
    ) -> dict:
        print("~~~*~~~*~~~*~~~*~~~*~~~*~~~ create user request ~~~*~~~*~~~*~~~*~~~*~~~*~~~")
        if password != password_confirmation:
            print ("password_confirmation_mismatch")
            raise BadRequestException(message="Error: password confirmation mismatch.")
        
        email, phone = validation(email=email, phone="")
        
        try:
            hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = select(User).where(
                    and_(User.email == email, User.deleted_at == None))
            result = await session.execute(query)
            does_exist = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        if does_exist:
            print ("email_exists")
            raise DuplicateValueException(message="Error: email already exists.")
        
        try:
            print("database accessed")
            ts = now()
            user = User(email=email, password=hash, name=name, user_type="member")
            session.add(user)
        except Exception as e:
            raise UnprocessableEntity(e.args[0])

        print("create user success")
        return {
            "success": True,
            "message": "User created successfully.",
            "token": TokenHelper.encode(payload={"nonce": random.randint(100000, 999999)}, expire_period=300),
        }

    @Transactional()
    async def update_user(
        self,
        name: str,
        user_id: int,
    ) -> dict:
        try:
            ts = now()
            print("~~~~~~~~~~~~~~~~~~~~~~~ update user request")
            query = select(User).where(
                User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        user_availability(user=user)
        user.name = name if name else user.name
        
        print("update user success")
        return {
            "success": True,
            "message": "User has been updated successfully."
        }

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()
        if not user:
            return False
        if user.user_type != "admin":
            return False
        if user.deleted_at:
            return False
        return True

    @Transactional()
    async def login(
        self,
        email: str,
        password: str,
    ) -> LoginResponseSchema:
        print("~~~~~~~~~~~~~~~~~~~~~~~ login request")
        ts = now()
        email, phone = validation(email=email, phone="")
        query = select(User).where(
                and_(User.email == email, User.deleted_at == None))
        result = await session.execute(query)
        user = result.scalars().first()
        
        user_availability(user=user)
        if not bcrypt.checkpw(password.encode('utf-8'), str(user.password).encode('utf-8')):
            raise UnauthorizedException(message="Invalid username of password.")
        
        print(user.id, user.email, password)
        print("login request success")
        response = {
            "success": True,
            "message": "Login successfully.",
            "token": TokenHelper.encode(payload={"user_id": user.id, "name": user.name}),
            "refresh_token": TokenHelper.encode(payload={"sub": "refresh"}),
        }
        return response

    @Transactional()
    async def forgot_password(
        self,
        email: str,
    ) -> dict:
        print("~~~~~~~~~~~~~~~~~~~~~~~ forgot password request")
        email, phone = validation(email=email, phone="")
        try:
            query = select(User).where(
                and_(User.email == email, User.deleted_at == None))
            result = await session.execute(query)
            user = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        user_availability(user=user)

        print("forgot password success")
        return {
            "success": True,
            "message": "Email verification code sent successfully.",
            "token": TokenHelper.encode(payload={"nonce": random.randint(100000, 999999)}, expire_period=300),
        }

    @Transactional()
    async def reset_password(
        self,
        token: str,
        new_password1: str,
        new_password2: str,
    ) -> dict:
        print("~~~~~~~~~~~~~~~~~~~~~~~ reset password request")
        id = TokenHelper.decode(token=token).get('user_id')
        try:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        user_availability(user=user)
        if new_password1 != new_password2:
            raise UnprocessableEntity(message="Error: password confirmation mismatch.")
        
        try:
            hash = bcrypt.hashpw(new_password1.encode('utf-8'), bcrypt.gensalt())
            user.password = hash
            user.verification_code = None
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        print("reset password success")
        return {
            "success": True,
            "message": "Password has been reset successfully.",
            "token": TokenHelper.encode(payload={"user_id": user.id, "name": user.name}),
            "refresh_token": TokenHelper.encode(payload={"sub": "refresh"}),
        }

    @Transactional()
    async def change_password(
        self,
        user_id: int,
        password: str,
        new_password1: str,
        new_password2: str,
    ) -> ChangePasswordResponseSchema:
        try:
            print("~~~~~~~~~~~~~~~~~~~~~~~ change password request")
            if new_password1 != new_password2:
                raise BadRequestException(message="Error: password confirmation mismatch.")
            result = await session.execute(
                select(User).where(
                    User.id == user_id)
            )
            user = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        user_availability(user=user)

        if not bcrypt.checkpw(password.encode('utf-8'), str(user.password).encode('utf-8')):
            raise UnauthorizedException(message="Error: incorrect password.")
        
        try:
            hash = bcrypt.hashpw(new_password1.encode('utf-8'), bcrypt.gensalt())
            user.password = hash
        except Exception as e:
            raise UnprocessableEntity(e.args[0])

        print("change password success")
        return { "success": True, "message": "Password has been changed successfully." }

    @Transactional()
    async def delete(
        self,
        user_id: int,
    ) -> None:
        try:
            print("~~~~~~~~~~~~~~~~~~~~~~~ delete user request")
            result = await session.execute(
                select(User).where(and_(User.id == user_id, User.deleted_at == None))
            )
            user = result.scalars().first()
        except Exception as e:
            raise UnprocessableEntity(e.args[0])
        
        user_availability(user=user)
        
        try:
            # await session.delete(user)
            user.deleted_at = now()
        except Exception as e:
            raise UnprocessableEntity(message=e.args[0])
        
        print("delete user success")
        return { "success": True, "message": "User has been deleted successfully." }
    