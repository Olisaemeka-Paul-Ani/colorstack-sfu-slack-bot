import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Check if tokens are loaded
bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

print(f"Bot token loaded: {bot_token[:10]}..." if bot_token else "Bot token MISSING")
print(f"App token loaded: {app_token[:10]}..." if app_token else "App token MISSING")

app = App(token=bot_token)

@app.event("member_joined_channel")
def handle_member_joined(event, client):
    user_id = event["user"]
    user_info = client.users_info(user=user_id)
    user_name = user_info["user"]["real_name"]
    
    welcome_message = f"Hey {user_name}! 👋 Welcome to ColorStack SFU! We're excited to have you here. Feel free to introduce yourself in #general and check out our upcoming events in #events!"
    
    client.chat_postMessage(
        channel=user_id,
        text=welcome_message
    )
    
    print(f"Sent welcome message to {user_name}")

if __name__ == "__main__":
    print("⚡️ Bot starting in Socket Mode...")
    try:
        handler = SocketModeHandler(app, app_token)
        print("Socket handler created successfully")
        handler.start()
    except Exception as e:
        print(f"Error starting bot: {e}")