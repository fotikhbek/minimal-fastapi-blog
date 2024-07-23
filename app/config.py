from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

BASE_DIR = Path(__file__).parent.parent
abs_path = BASE_DIR / ".env"


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=abs_path, env_file_encoding="utf-8")


@lru_cache(typed=True)
def load_settings() -> Settings:
    return Settings()


@lru_cache(typed=True)
def load_auth_jwt() -> AuthJWT:
    return AuthJWT()
