# Tokens y rutas de carpetas
import os
import dotenv

dotenv.load_dotenv()

def get_user_id(user_id: str) -> int | None:
    value = os.getenv(user_id)

    if value is None:
        return None

    try:
        return int(value)
    except TypeError:
        return None

def collect_info_by_env(env_name: str) -> str | None:
    return os.getenv(env_name)