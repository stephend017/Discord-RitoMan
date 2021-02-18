import os


class BaseConfig:
    """
    The base definition of a config type
    """

    DB_URI_BASE = "postgresql://"
    DB_USER = "root"
    DB_PASS = "root"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "rito"
    DEBUG = True
    TESTING = True
    RIOT_TOKEN = ""
    DISCORD_WEBHOOK = ""


class TestingConfig:
    """
    The config used for testing and development
    """

    DB_URI_BASE = "postgresql"
    DB_USER = "docker"
    DB_PASS = "docker"
    DB_HOST = "localhost"
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = "ritoman_test"
    DEBUG = True
    TESTING = True
    RIOT_TOKEN = "mock_riot_token"
    DISCORD_WEBHOOK = "mock_discord_webhook"


class ProductionConfig:
    """
    The config used for production
    """

    DB_URI_BASE = "postgresql"
    DB_USER = "root"
    DB_PASS = os.getenv("DB_PASS", "error")
    DB_HOST = "localhost"
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = "rito"
    DEBUG = False
    TESTING = False
    RIOT_TOKEN = os.getenv("RIOT_TOKEN", "token")
    DISCORD_WEBHOOK = os.getenv("DISCORD_BOT", "webhook")
