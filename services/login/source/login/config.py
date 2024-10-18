import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path

# Load Env variables
load_dotenv()


def get_env_str(env_var: str) -> str:
    return os.getenv(env_var)


def get_env_int(env_var: str) -> int:
    return int(os.getenv(env_var))


def get_env_float(env_var: str) -> float:
    return float(os.getenv(env_var))


def get_env_bool(env_var: str) -> str:
    return os.getenv(env_var, "False").lower() in ("true", "1", "t")


def get_env_path(env_var: str) -> Path:
    if os.getenv(env_var) is None:
        return None
    else:
        return Path(os.getenv(env_var))


def get_env_choise(env_var: str, choises: list[str]) -> str:
    choise = os.getenv(env_var)
    if not choise in choises:
        raise ValueError(f"Value for {env_var} not valid! Must be one of: {choises}")
    return choise


@dataclass(frozen=False)
class Config:
    config_path: Path = field(default=get_env_path("CONFIG_PATH"))
    log_level: str = get_env_str("LOG_LEVEL").upper()
    secret: str = get_env_str("SECRET")
    mongo_host: str = get_env_str("MONGO_HOST")
    mongo_port: int = get_env_int("MONGO_PORT")
    mongo_user: str = get_env_str("MONGO_USER")
    mongo_pass: str = get_env_str("MONGO_PASS")
    redis_host: str = get_env_str("REDIS_HOST")
    redis_port: str = get_env_str("REDIS_PORT")

