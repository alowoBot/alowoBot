import asyncio
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat
from twitchAPI.type import ChatEvent

import credentials
from events import on_ready, on_message, set_context_globals
from token_utils import authenticate_or_load

APP_ID     = credentials.get_appId()
APP_SECRET = credentials.get_appSecret()
SCOPES     = [
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT,
    AuthScope.CHANNEL_MANAGE_BROADCAST,
    AuthScope.CHANNEL_MODERATE,
    AuthScope.MODERATOR_MANAGE_CHAT_MESSAGES,
    AuthScope.MODERATOR_MANAGE_BANNED_USERS
]

async def run_bot():
    twitch = await Twitch(APP_ID, APP_SECRET)

    token, refresh = await authenticate_or_load(twitch, SCOPES)

    await twitch.set_user_authentication(token, SCOPES, refresh)

    bot_user = await anext(twitch.get_users())
    moderator_id = bot_user.id

    target_channel_login = credentials.get_targetChannel()
    broadcaster_user = await anext(twitch.get_users(logins=[target_channel_login]))
    broadcaster_id = broadcaster_user.id

    print(f"BotID: {moderator_id}")
    print(f"Target Channel: {broadcaster_user.display_name} (ID: {broadcaster_id})")

    set_context_globals(
        twitch_instance=twitch,
        token=token,
        client_id=APP_ID,
        broadcaster_id=broadcaster_id,
        moderator_id=moderator_id
    )

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()

    try:
        input("Press Enter to stop...\n")
    finally:
        chat.stop()
        await twitch.close()

def main():
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
