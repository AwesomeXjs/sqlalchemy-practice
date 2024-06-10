from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_USER: str
    DB_HOST: str

    DB_HOST_alembic: str
    DB_NAME_alembic: str
    DB_PASS_alembic: str
    DB_PORT_alembic: int
    DB_USER_alembic: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER_alembic}:{self.DB_PASS_alembic}@{self.DB_HOST_alembic}:{self.DB_PORT_alembic}/{self.DB_NAME_alembic}"

    @property
    def database_url_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER_alembic}:{self.DB_PASS_alembic}@{self.DB_HOST_alembic}:{self.DB_PORT_alembic}/{self.DB_NAME_alembic}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
