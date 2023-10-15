from sqlalchemy import Column, String, BigInteger, TIMESTAMP

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_type = Column(String(10), nullable=False, default="member")
    name = Column(String(191), nullable=False, unique=False)
    email = Column(String(191), nullable=True, unique=True)
    password = Column(String(191), nullable=False)
    remember_token = Column(String(100), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)