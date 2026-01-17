import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import google.generativeai as genai

# 1. Load credentials
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])

# 2. Helper: Find Channel ID by Name
def get_channel_id(name):
    result = app.client.conversations_list()
    for channel in result["channels"]:
        if channel["name"] == name:
            return channel["id"]
    return None

# 3. The Command Handler
@app.command("/catchup")
def handle_command(ack, body, respond):
    ack() # Acknowledge Slack immediately
    
    channel_name = body['text'].strip().replace('#', '')
    channel_id = get_channel_id(channel_name)
    
    if not channel_id:
        respond(f"Could not find channel: #{channel_name}")
        return

    # Fetch last 100 messages
    result = app.client.conversations_history(channel=channel_id, limit=100)
    messages = result["messages"]
    
    # Format text for the AI
    chat_history = ""
    for msg in reversed(messages):
        user = msg.get("user", "Unknown")
        text = msg.get("text", "")
        chat_history += f"User {user}: {text}\n"

    # 4. Summarize with Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an executive assistant. Summarize the following Slack messages from #{channel_name}.
    - Provide a 3-sentence high-level summary.
    - List 'Action Items' or 'Decisions Made'.
    - Highlight if the user '{body['user_id']}' was mentioned or asked to do something.
    
    Messages:
    {chat_history}
    """
    
    response = model.generate_content(prompt)
    
    # 5. Send private response
    respond(f"Here is your catch-up for *#{channel_name}*:\n\n{response.text}")

if __name__ == "__main__":
    # Socket Mode allows you to run locally without a public URL
    handler = SocketModeHandler(app, os.environ["SLACK_APP_LEVEL_TOKEN"])
    handler.start()