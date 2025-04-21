# <img src="assets/owo.png" width="24" /> alowoBot
### By [vfsas3](https://github.com/vfsas3)
A Twitch moderation bot that enforces good vibes and proper emote etiquette — with some AI magic.


![alowo](https://cdn.7tv.app/emote/01H7AXNHM0000466AJ0H5AD484/4x.webp)

---

## ✨ Features

- **Toxic message detection** using [Perspective API](https://perspectiveapi.com/)
- **Automatic timeouts and bans** based on toxicity levels
- **7TV emote typo detection** (timeouts for scuffed spelling)
- Toggleable **strict mode** for emote spelling
- `!strict` command (moderators only)
- Fully async + powered by [twitchAPI](https://github.com/Teekeks/pyTwitchAPI)

---

![owola](https://cdn.7tv.app/emote/01H9GF23C80008QVVK15MGHQJX/4x.webp)

## ⚙️ Setup Guide

Follow these steps to get alowoBot up and running.

---

### 1. 🧪 Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A Twitch account
- A Google account
- [Perspective API access](https://developers.perspectiveapi.com/s/docs-get-started)

---

### 2. 📦 Step by Step
  
```alowoBot/
  │
  ├── .env  👈 create this
  ├── alowoBot/
  ├── requirements.txt
  ├── ...

  APP_ID=your_twitch_app_id -> https://dev.twitch.tv/console
  APP_SECRET=your_twitch_app_secret -> https://dev.twitch.tv/console
  TARGET_CHANNEL=your_channel_name -> target channel
  PERSPECTIVE_KEY=your_perspective_api_key -> googlecloud->console->perspectiveApi (may need to get access)


