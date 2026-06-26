from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "LABCENTER"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8900
    APP_DEBUG: bool = False
    DATABASE_URL: str
    JWT_SECRET: str
    LDAP_SERVER: str
    LDAP_DOMAIN: str
    LOG_PATH: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()