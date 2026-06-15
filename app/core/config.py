from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pfand Counter API"
    auth_enabled: bool = False
    database_url: str = "sqlite:///./pfand.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()