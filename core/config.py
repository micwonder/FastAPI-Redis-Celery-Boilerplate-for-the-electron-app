import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"
    READER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"
    JWT_SECRET_KEY: str = "e168f2e2ec66fe69378dc2f33a3ec2a1143a52ab98ca791c0b1e9a0918742e64"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = None
    CELERY_BACKEND_URL: str = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"
    READER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"
    READER_DB_URL: str = f"mysql+aiomysql://root:123456@localhost:3306/beta_projectx_db"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mysql+aiomysql://projectx:techguru@0.0.0.0:3306/projectx"
    READER_DB_URL: str = f"mysql+aiomysql://projectx:techguru@0.0.0.0:3306/projectx"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
