import json
import os
import requests
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope

TOKEN_FILE = "tokens.json"

async def authenticate_or_load(twitch, scopes: list[AuthScope]):
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            twitch.access_token = data["token"]
            twitch.refresh_token = data["refresh"]
            return data["token"], data["refresh"]
    else:
        auth = UserAuthenticator(twitch, scopes)
        token, refresh_token = await auth.authenticate()
        with open(TOKEN_FILE, "w") as f:
            json.dump({"token": token, "refresh": refresh_token}, f)
        twitch.access_token = token
        twitch.refresh_token = refresh_token
        return token, refresh_token

def timeout_user_api(token: str, client_id: str, broadcaster_id: str, moderator_id: str, target_user_id: str, duration_seconds: int = 10, reason: str = "Toxic message"):
    url = "https://api.twitch.tv/helix/moderation/bans"

    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }

    payload = {
        "broadcaster_id": broadcaster_id,
        "moderator_id": moderator_id,
        "data": {
            "user_id": target_user_id,
            "duration": duration_seconds,
            "reason": reason
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ User {target_user_id} timed out for {duration_seconds}s")
    else:
        print(f"❌ Timeout failed: {response.status_code} {response.text}")

def ban_user_api(token: str, client_id: str, broadcaster_id: str, moderator_id: str, target_user_id: str, reason: str = "Toxic message"):
    url = "https://api.twitch.tv/helix/moderation/bans"

    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id,
        "Content-Type": "application/json"
    }

    payload = {
        "broadcaster_id": broadcaster_id,
        "moderator_id": moderator_id,
        "data": {
            "user_id": target_user_id,
            "reason": reason
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ User {target_user_id} banned permanently")
    else:
        print(f"❌ Ban failed: {response.status_code} {response.text}")
