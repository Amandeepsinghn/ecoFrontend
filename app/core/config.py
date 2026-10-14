import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL")

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY") #private key
    jwt_algorithm : str = os.getenv("JWT_ALGORITHM", "HS256") #signing algorithm
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    ) #how long it will remain valid


settings = Settings()