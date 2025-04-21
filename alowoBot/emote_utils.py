import requests
import credentials
import asyncio
from twitchAPI.twitch import Twitch

STRICT_MODE = True 
EMOTE_LIST = []

def get_strict_mode():
    return STRICT_MODE

def set_strict_mode(state: bool):
    global STRICT_MODE
    STRICT_MODE = state
    print(f"🔧 Strict mode set to: {STRICT_MODE}")

async def fetch_7tv_emotes():
    twitch_user_id = await get_twitch_user_id()
    emotes = get_7tv_emotes(twitch_user_id)
    global EMOTE_LIST
    EMOTE_LIST = emotes
    print(f"Loaded {len(emotes)} emotes from 7TV {twitch_user_id} emote pack.")
    print("→ Emotes:", EMOTE_LIST)
    return emotes

async def get_twitch_user_id():
    twitch = await Twitch(credentials.get_appId(), credentials.get_appSecret())
    user = await anext(twitch.get_users(logins=[credentials.get_targetChannel()]), None)
    if user is None:
        raise Exception(f"Twitch user '{credentials.get_targetChannel()}' not found")
    return user.id

def get_7tv_emotes(twitch_user_id):
    url = f"https://api.7tv.app/v3/users/twitch/{twitch_user_id}"
    res = requests.get(url)

    if res.status_code != 200:
        print(f"Failed to fetch 7TV user: {res.status_code}")
        return []

    data = res.json()
    emote_set = data.get("emote_set")

    if not emote_set:
        print("No emote set found. Make sure there is a active emote set")
        return []

    return [emote["name"] for emote in emote_set.get("emotes", [])]

def check_for_emote_typos(message: str):
    from difflib import get_close_matches
    words = message.split()
    mistakes = []

    for word in words:
        matches = get_close_matches(word, EMOTE_LIST, n=1, cutoff=0.7 if STRICT_MODE else 0.9)
        if matches and matches[0] != word:
            mistakes.append((word, matches[0]))

    print(f"Checking for typos in: {message}")
    print(f"Typos found: {mistakes}")
    return mistakes
