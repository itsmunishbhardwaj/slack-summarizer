import os
import time
import datetime
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

def summarize_messages(client, channel_id, user_id, messages, thread_ts=None, date_range=None):
    """Common function to summarize messages for both threads and channels"""
    try:
        # Get user name with fallback
        user_info = client.users_info(user=user_id)
        real_name = user_info['user']['profile'].get('real_name', 'Team Member')

        # Cache for usernames to avoid duplicate API calls
        user_cache = {}
        
        def get_username(uid):
            if uid not in user_cache:
                try:
                    user_info = client.users_info(user=uid)
                    user_cache[uid] = user_info['user']['profile'].get('real_name', uid)
                except:
                    user_cache[uid] = uid
            return user_cache[uid]

        # Build chat history with usernames
        chat_history = ""
        mentions_history = ""
        mention_count = 0
        mention_links = []  # Store links to messages with mentions
        
        for msg in reversed(messages):
            if "text" in msg and "user" in msg:
                username = get_username(msg['user'])
                message_text = msg['text']
                chat_history += f"{username}: {message_text}\n"
                
                # Check if this message mentions the user
                if f"<@{user_id}>" in message_text:
                    mentions_history += f"{username}: {message_text}\n"
                    mention_count += 1
                    
                    # Get permalink for this message
                    try:
                        permalink_response = client.chat_getPermalink(
                            channel=channel_id,
                            message_ts=msg['ts']
                        )
                        mention_links.append({
                            'username': username,
                            'link': permalink_response['permalink'],
                            'text': message_text
                        })
                        # Small delay to respect Slack's rate limits
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"⚠️ Could not get permalink: {e}")

        # AI Prompt with structured output
        prompt = f"""Summarize these Slack messages for {real_name}. Keep it concise and actionable.

Format your response EXACTLY as follows with proper spacing:

*📋 Summary*

• [Key point 1]

• [Key point 2]

• [Key point 3]


*🎯 Action Items*

• [Action item 1 - if none, write "None at this time"]

• [Action item 2 if any]


Messages:
{chat_history}"""

        # Build mentions section separately with inline links if there are any
        mentions_section = ""
        if mention_count > 0:
            mentions_section = "\n\n\n*🔔 Messages Mentioning You*\n\n"
            for i, mention in enumerate(mention_links, 1):
                # Clean message text
                clean_text = mention['text'].replace(f"<@{user_id}>", "you")
                if len(clean_text) > 100:
                    clean_text = clean_text[:97] + "..."
                # Add bullet with embedded link
                mentions_section += f"• <{mention['link']}|{mention['username']}: {clean_text}>\n\n"
            
            # Also add context to AI prompt
            prompt += f"""

**IMPORTANT:** There are {mention_count} message(s) where {real_name} was directly mentioned. Summarize the ACTION ITEMS from these mentions specifically.

Mentioned Messages:
{mentions_history}"""

        response = model.generate_content(prompt)
        
        # Build summary header
        if date_range:
            summary_text = f"✨ *Summary ({date_range})*\n\n"
        else:
            summary_text = f"✨ *Thread Summary*\n\n"
        
        summary_text += f"_{len(messages)} messages_\n\n\n"
        summary_text += response.text
        
        # Append mentions section with embedded links
        summary_text += mentions_section
        
        # Send the summary
        if thread_ts:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                thread_ts=thread_ts,
                text=summary_text
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=summary_text
            )

    except Exception as e:
        print(f"❌ Error during summarization: {e}")

@app.command("/catchup")
def handle_command(ack, body, client):
    ack()
    
    channel_id = body["channel_id"]
    user_id = body["user_id"]
    
    # Check if command was called in a thread
    thread_ts = body.get("thread_ts") or body.get("message", {}).get("thread_ts")
    
    if thread_ts:
        # Handle thread summarization directly
        try:
            client.chat_postEphemeral(channel=channel_id, user=user_id, thread_ts=thread_ts, text=f"🔍 Reading thread messages...")
            
            # Fetch thread messages
            result = client.conversations_replies(channel=channel_id, ts=thread_ts)
            messages = result["messages"]
            
            if not messages:
                client.chat_postEphemeral(channel=channel_id, user=user_id, thread_ts=thread_ts, text="No messages found in this thread.")
                return
            
            # Process thread messages
            summarize_messages(client, channel_id, user_id, messages, thread_ts=thread_ts)
            
        except Exception as e:
            print(f"❌ Error processing thread: {e}")
    else:
        # Show modal for channel-wide summarization
        trigger_id = body["trigger_id"]
        today = datetime.datetime.now()
        week_ago = today - datetime.timedelta(days=7)

        try:
            client.views_open(
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "callback_id": "date_selection_modal",
                    "private_metadata": channel_id,
                    "title": {"type": "plain_text", "text": "Catch Up"},
                    "submit": {"type": "plain_text", "text": "Summarize"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "start_date_block",
                            "element": {"type": "datepicker", "action_id": "start_date", "initial_date": week_ago.strftime('%Y-%m-%d')},
                            "label": {"type": "plain_text", "text": "Start Date"}
                        },
                        {
                            "type": "input",
                            "block_id": "end_date_block",
                            "element": {"type": "datepicker", "action_id": "end_date", "initial_date": today.strftime('%Y-%m-%d')},
                            "label": {"type": "plain_text", "text": "End Date"}
                        }
                    ]
                }
            )
        except Exception as e:
            print(f"❌ Error opening modal: {e}")

@app.view("date_selection_modal")
def handle_view_submission(ack, body, client, view):
    ack()
    
    user_id = body["user"]["id"]
    channel_id = view["private_metadata"]
    
    try:
        # Get dates
        state_values = view["state"]["values"]
        start_str = state_values["start_date_block"]["start_date"]["selected_date"]
        end_str = state_values["end_date_block"]["end_date"]["selected_date"]
        
        oldest = time.mktime(datetime.datetime.strptime(start_str, "%Y-%m-%d").timetuple())
        latest = time.mktime(datetime.datetime.strptime(end_str, "%Y-%m-%d").timetuple()) + 86399

        client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"🔍 Reading messages...")

        # Fetch History
        result = client.conversations_history(channel=channel_id, oldest=str(oldest), latest=str(latest))
        messages = result["messages"]
        
        if not messages:
            client.chat_postEphemeral(channel=channel_id, user=user_id, text="No messages found in that range.")
            return

        # Use the common summarization function
        date_range = f"{start_str} to {end_str}"
        summarize_messages(client, channel_id, user_id, messages, date_range=date_range)

    except Exception as e:
        print(f"❌ Error during submission: {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_LEVEL_TOKEN"])
    handler.start()
