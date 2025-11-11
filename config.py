from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = '/Users/ruslan/PycharmProjects/human-in-the-loop-intro/.env'

class Settings(BaseSettings):
    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()