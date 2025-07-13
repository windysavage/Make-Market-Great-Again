from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TRUTHSOCIAL_USERNAME: str
    TRUTHSOCIAL_PASSWORD: str

    OPENAI_API_KEY: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str

    model_config = SettingsConfigDict(
        env_file=('.env'), env_file_encoding='utf-8', case_sensitive=True
    )


def get_settings() -> BaseSettings:
    return Settings()
