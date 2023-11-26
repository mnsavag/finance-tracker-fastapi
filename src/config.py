from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int | str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    db_echo: bool = True

    model_config = SettingsConfigDict(env_file="/.env")

    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
