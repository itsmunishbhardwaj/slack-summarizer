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
1. Socket Mode: Enable it in your Slack App settings.
2. Slash Commands: Create a new command /catchup.
3. Scopes: Add channels:history, groups:history, users:read, and commands under OAuth & Permissions.
4. Event Subscriptions: Enable and subscribe to message.channels.

### 5. Run the Bot
```bash
python main.py
```

## 📖 Usage
1. Invite the bot to your desired channel: /invite @CatchUpBot.
2. In any chat, type: /catchup #general.
3. The bot will fetch the latest history, process it through Gemini, and post a private summary like this:
    **Summary for #general:**
   - The team decided to move the launch date to Friday.
   - Action Item for You: Review the design doc shared by @Sarah.

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.
