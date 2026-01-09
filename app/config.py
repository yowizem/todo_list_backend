from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str
    DATABASE: str
    USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
