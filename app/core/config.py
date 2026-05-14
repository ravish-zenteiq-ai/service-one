from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    db_username: str
    db_port: str
    db_password: str
    db_name: str
    db_hostname: str
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file= ".env"
        



settings = AppConfig()

    