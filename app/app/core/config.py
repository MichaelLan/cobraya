from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'CobraYA'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'b0Dcf437fd5b42c509c8f8025ece0cf368ebe051c242f80015cace1fb31d11dc'

    DEGUG: bool = True

    HOST: str = '127.0.0.1'
    PORT: int = 8080

    # Database
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///./{PROJECT_NAME.lower()}.sqlite3"


settings = Settings()
