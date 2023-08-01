import os


def env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise KeyError(
            f"must provide a '{key}' variable in the environment or .env file")

    return value


def env_or(key: str, default: str = "") -> str:
    value = os.getenv(key)
    if value is None:
        return default

    return value
