from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_CLUSTER_URL: str

    ALGORITHM: str
    SECRET_KEY: str

    DATABASE_NAME: str
    HOST: str
    PASSWORD: str
    USERNAME: str
    DATABASE_URL: str
    TESTING_DATABASE_URL: str
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings() # type: ignore[call-arg]


