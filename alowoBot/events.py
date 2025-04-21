from twitchAPI.chat import ChatMessage, EventData
from twitchAPI.twitch import Twitch
from timeout_utils import timeout_test
from token_utils import timeout_user_api, ban_user_api
import credentials
from emote_utils import fetch_7tv_emotes, check_for_emote_typos, set_strict_mode, get_strict_mode

TARGET_CHANNEL = credentials.get_targetChannel()

TWITCH = None
TOKEN = None
CLIENT_ID = None
BROADCASTER_ID = None
MODERATOR_ID = None
CHAT = None

def set_context_globals(twitch_instance, token, client_id, broadcaster_id, moderator_id):
    global TWITCH, TOKEN, CLIENT_ID, BROADCASTER_ID, MODERATOR_ID
    TWITCH = twitch_instance
    TOKEN = token
    CLIENT_ID = client_id
    BROADCASTER_ID = broadcaster_id
    MODERATOR_ID = moderator_id

async def on_ready(event: EventData):
    global CHAT
    CHAT = event.chat
    await event.chat.join_room(TARGET_CHANNEL)
    await fetch_7tv_emotes()
    set_strict_mode(True)  # strict mode enabled on startup
    await event.chat.send_message(TARGET_CHANNEL, "ALOWO alowo")
    print(f"Joined {TARGET_CHANNEL}")

async def on_message(msg: ChatMessage):
    global BROADCASTER_ID, MODERATOR_ID, TWITCH

    print(f"{msg.user.display_name}: {msg.text}")

    # !strict command (toggle strict mode)
    if msg.text.strip().lower() == "!strict":
        is_mod = "moderator" in msg.user.badges
        is_broadcaster = msg.user.id == BROADCASTER_ID

        if is_mod or is_broadcaster:
            current_mode = get_strict_mode()
            new_mode = not current_mode
            set_strict_mode(new_mode)
            await msg.chat.send_message(TARGET_CHANNEL, f"Strict mode is now {'ON. Watch out for MinorSpellingMistake ' if new_mode else "OFF. Dont't fuck around to much or i'll reactivate it Smile "}.")
        else:
            await msg.chat.send_message(TARGET_CHANNEL, "You're not a moderator jackass.")
        return

    # Emote typo detection
    typos = check_for_emote_typos(msg.text)
    if typos:
        typo_report = ", ".join([f"{wrong} → {correct}" for wrong, correct in typos])
        print(f"  → Emote typos detected: {typo_report}")
        if any(len(wrong) >= 4 and wrong.lower() != correct.lower() for wrong, correct in typos):
            await msg.chat.send_message(TARGET_CHANNEL, f"GAGAGA {msg.user.name} just did a MinorSpellingMistake  ({typo_report})")
            username = msg.user.name.lower()
            user_data = await anext(TWITCH.get_users(logins=[username]), None)
            if user_data:
                timeout_user_api(
                    token=TOKEN,
                    client_id=CLIENT_ID,
                    broadcaster_id=BROADCASTER_ID,
                    moderator_id=MODERATOR_ID,
                    target_user_id=user_data.id,
                    duration_seconds=20,
                    reason=f"Emote typo: {typo_report}"
                )
            return

    # Perspective API toxicity check
    flagged, label, score = timeout_test(msg.text)
    print(f"  → Label: {label}, Score: {score:.2f}")

    if not flagged:
        print("  → Clean")
        return

    username = msg.user.name.lower()
    print(f"🔍 Looking up user: {username}")

    user_data = await anext(TWITCH.get_users(logins=[username]), None)

    if user_data is None:
        print(f"Could not find user ID for {username}")
        await msg.chat.send_message(TARGET_CHANNEL, f"Could not find user ID for {username}")
        return

    target_user_id = user_data.id
    print(f"Found user ID {target_user_id} for {username}")

    try:
        if score >= 0.85:
            ban_user_api(
                token=TOKEN,
                client_id=CLIENT_ID,
                broadcaster_id=BROADCASTER_ID,
                moderator_id=MODERATOR_ID,
                target_user_id=target_user_id,
                reason=f"Toxic (ban): {label} ({score:.2f})"
            )
            await msg.chat.send_message(TARGET_CHANNEL, f"{username} has been banned for misbehaving (reason: {label}).")
            print(f"🚫 Banned {username} for {label} ({score:.2f})")
        elif score >= 0.7:
            timeout_user_api(
                token=TOKEN,
                client_id=CLIENT_ID,
                broadcaster_id=BROADCASTER_ID,
                moderator_id=MODERATOR_ID,
                target_user_id=target_user_id,
                duration_seconds=60,
                reason=f"{label}"
            )
            await msg.chat.send_message(TARGET_CHANNEL, f"{username} has been timed-out for misbehaving (reason: {label}).")
            print(f"⏱️  Timed out {username} for {label} ({score:.2f})")
        else:
            print("⚠️ Flagged but below timeout threshold")

    except Exception as e:
        print(f"❌ Moderation action failed: {e}")
        await msg.chat.send_message(TARGET_CHANNEL, f"❌ Moderation failed for {username}")
