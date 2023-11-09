import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

def load_secrets():
    """
    Function to get api keys from .env files. More api key scan be added and returned.
    """
    load_dotenv()
    # env_path = Path(__file__).parent.parent.parent / "keys.env"
    load_dotenv(find_dotenv())

    open_ai_key = os.getenv("OPENAI_API_KEY")
    print("OPEN AI KEY: ",open_ai_key)

    return {
        "OPENAI_API_KEY": open_ai_key
    }
load_secrets()