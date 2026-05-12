# Tokens y rutas de carpetas
import os
import dotenv

dotenv.load_dotenv()

def get_user_id():
    try:
        return int(os.getenv("USER_ID"))
    except KeyError:
        return None

def get_token():
    try:
        return os.getenv("TOKEN")
    except KeyError:
        return None

def get_label_mount():
    try:
        return os.getenv("LABEL_MOUNT")
    except KeyError:
        return None