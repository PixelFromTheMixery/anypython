# region Docs
"""
Settings for the rest of the app

Anytype connection setup

Classes:
    EnvSettings(BaseSettings): Uses env variables to be used in other areas

Methods:
    fetch_settings: lru_cached settings object fetcher
"""
# endregion

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    # region Docs
    """
    Uses env variables to be used in other areas

    Attributes:
        key (str): API key to be used to make calls
        url (str): url to call anytype via, default: "localhost"
        port (str): port through which api to run, uses headless default
        logger (bool): use local logger
    """

    # endregion

    anypython_key: str
    anypython_url: str = "localhost"
    anypython_port: str = "31012"
    anypython_logger: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def fetch_settings() -> EnvSettings:
    # region Docs
    """
    lru_cached settings object fetcher

    Returns:
        EnvSettings: env variables wrapped nicely and not regenerated
    """
    # endregion

    return EnvSettings()
