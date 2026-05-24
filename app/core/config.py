#  it validates that your settings exist
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    This class loads variables from the .env file.
    It provides type safety for our configuration.
    """
    PROJECT_NAME : str
    DATABASE_URL: str

    # This tells Pydantic to look for a file named ".env"
    model_config = SettingsConfigDict(env_file=".env")

# We instantiate this once so we can import 'settings' anywhere
settings = Settings()