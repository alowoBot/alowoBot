from dotenv import load_dotenv
import os

load_dotenv()

def get_appId():
    return os.getenv("TWITCH_APP_ID")

def get_appSecret():
    return os.getenv("TWITCH_APP_SECRET")

def get_perspectiveKey():
    return os.getenv("PERSPECTIVE_API_KEY")

def get_targetChannel():
    return "d4rkycode"
