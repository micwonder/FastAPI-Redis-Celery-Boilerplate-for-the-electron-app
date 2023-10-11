from app.auth.schemas.jwt import RefreshTokenSchema
from core.exceptions.token import DecodeTokenException
from core.utils.token_helper import TokenHelper


class JwtService:
    async def verify_token(
        self,
        token: str,
    ) -> None:
        TokenHelper.decode(token=token)

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenSchema:
        token = TokenHelper.decode_expired_token(token=token)
        refresh_token = TokenHelper.decode_expired_token(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise DecodeTokenException
        
        user_id = token.get("user_id")
        name = token.get("name")
        print ("user_id:", user_id)
        print ("Welcome,", name)

        return RefreshTokenSchema(
            token=TokenHelper.encode(payload={"user_id": user_id, "name": name}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
