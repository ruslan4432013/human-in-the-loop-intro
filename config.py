from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = '.env'

class Settings(BaseSettings):
    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    OPENROUTER_API_KEY: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()