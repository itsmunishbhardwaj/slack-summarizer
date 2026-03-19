# 🚀 Slack CatchUp Bot

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange)](https://ai.google.dev/)

Coming back from a holiday to hundreds of Slack messages is overwhelming. **Slack CatchUp Bot** uses Google’s Gemini AI to scan your starred or important channels, summarize the conversations, and highlight exactly where you were mentioned or have pending action items.

---

## ✨ Features

* **Smart Summarization:** Condenses long, noisy chat histories into 3-4 high-level bullet points.
* **Personalized Highlights:** Uses your Slack User ID to find direct mentions or tasks assigned to you.
* **Privacy First:** Summaries are sent as *ephemeral* messages—only you can see the AI's response.
* **Slash Command Integration:** Simply type `/catchup #channel-name` to get up to speed.
* **Socket Mode:** Runs securely without needing a public URL or complex web server setup.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Framework:** [Slack Bolt for Python](https://tools.slack.dev/bolt-python/)
* **LLM:** [Google Gemini 1.5 Flash](https://ai.google.dev/)
* **Environment:** [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📋 Prerequisites

Before you begin, ensure you have:
1.  A **Slack Workspace** where you can create apps.
2.  A **Google AI Studio API Key** (Get it at [aistudio.google.com](https://aistudio.google.com/)).
3.  Python installed on your machine.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/slack-catchup-bot.git](https://github.com/your-username/slack-catchup-bot.git)
cd slack-catchup-bot
```
### 2. Set Up a Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a file named `.env` in the root folder and add your credentials:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_LEVEL_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your-signing-secret
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Configure Slack App Settings

#### A. Basic Settings
1. Go to [api.slack.com/apps](https://api.slack.com/apps) and select your app
2. Navigate to **Basic Information** → Copy the **Signing Secret**

#### B. Socket Mode Setup
1. Go to **Socket Mode** in the sidebar
2. Enable Socket Mode
3. Under "App-Level Tokens", generate a token with `connections:write` scope
4. Copy the token (starts with `xapp-`)

#### C. OAuth & Permissions (Bot Token Scopes)
Add the following **Bot Token Scopes** under **OAuth & Permissions**:
- `channels:history` - View messages in public channels
- `channels:read` - View basic channel info
- `chat:write` - **Required for sending ephemeral messages**
- `commands` - Add slash commands
- `groups:history` - View messages in private channels
- `groups:read` - View basic private channel info
- `users:read` - View user information

⚠️ **Important:** After adding scopes, you MUST click **"Reinstall to Workspace"** at the top of the OAuth & Permissions page to get a new token with these permissions.

#### D. Copy the New Bot Token
1. After reinstalling, copy the **Bot User OAuth Token** (starts with `xoxb-`)
2. This is your new `SLACK_BOT_TOKEN` for the `.env` file

#### E. Slash Commands
1. Go to **Slash Commands** in the sidebar
2. Click **Create New Command**
3. Command: `/catchup`
4. Short Description: "Summarize channel messages"
5. Save (Socket Mode handles the request URL automatically)

#### F. Install to Workspace
1. Go to **Install App** in the sidebar
2. Click **Install to Workspace** (or Reinstall if you've already installed it)
3. Authorize the permissions

### 5. Run the Bot
```bash
python main.py
```

## 📖 Usage
1. Invite the bot to your desired channel: /invite @CatchUpBot.
2. In any chat, type: /catchup
3. Select the date range in the modal that appears
4. The bot will fetch the history, process it through Gemini, and post a private summary like this:
    **Summary for #general:**
   - The team decided to move the launch date to Friday.
   - Action Item for You: Review the design doc shared by @Sarah.

---

## 🐛 Troubleshooting

### Error: `missing_scope` - `chat:write:bot` needed

**Problem:** You see an error like:
```
SlackApiError: The request to the Slack API failed.
The server responded with: {'ok': False, 'error': 'missing_scope', 'needed': 'chat:write:bot', 'provided': '...'}
```

**Solution:**
1. Go to [api.slack.com/apps](https://api.slack.com/apps) and select your app
2. Navigate to **OAuth & Permissions**
3. Verify all required scopes are added (see section 4.C above)
4. **Click "Reinstall to Workspace"** at the top of the page
5. After reinstalling, copy the NEW **Bot User OAuth Token** (starts with `xoxb-`)
6. Update your `.env` file with the new token
7. Restart the bot with `python main.py`

**Why this happens:** When you add new scopes to your Slack app, the existing bot token doesn't automatically get those permissions. You must reinstall the app to generate a new token with the updated scopes.

### Bot doesn't respond to `/catchup` command

**Possible causes:**
1. Socket Mode not enabled
2. App-Level Token missing or incorrect
3. Bot not invited to the channel

**Solution:**
1. Verify Socket Mode is enabled in your app settings
2. Check that `SLACK_APP_LEVEL_TOKEN` in `.env` is correct (starts with `xapp-`)
3. Invite the bot to the channel: `/invite @YourBotName`
4. Check the logs when running `python main.py` for error details

---

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.
