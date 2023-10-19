import os
from dotenv import load_dotenv
from pathlib import Path

def load_secrets():
    """
    Function to get api keys from .env files. More api key scan be added and returned.
    """
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    open_ai_key = os.getenv("OPENAI_API_KEY")

    palm_ai_key = os.getenv("PALM_API_KEY")

    return {
        "OPENAI_API_KEY": open_ai_key,
        "PALM_API_KEY": palm_ai_key
    }