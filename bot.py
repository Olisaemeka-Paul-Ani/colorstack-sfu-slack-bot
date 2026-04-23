import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import schedule
import time
import threading
import logging
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
# Check if tokens are loaded
bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

logging.info(f"Bot token loaded: {bot_token[:10]}..." if bot_token else "Bot token MISSING")
logging.info(f"App token loaded: {app_token[:10]}..." if app_token else "App token MISSING")

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


    logging.info(f"Sent welcome message to {user_name}")



def fetch_leetcode_daily():
    url = "https://leetcode.com/graphql"

    try:
        query = """
        query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
            title
            difficulty
            }
        }
        }
        """
        payload = {"query": query}
        response = requests.post(url, json=payload)
        data = response.json()
        title = data["data"]["activeDailyCodingChallengeQuestion"]["question"]["title"]
        link = data["data"]["activeDailyCodingChallengeQuestion"]["link"]
        difficulty = data["data"]["activeDailyCodingChallengeQuestion"]["question"]["difficulty"]

        hashMap = {
            "title": title,
            "link": f"https://leetcode.com{link}",
            "difficulty": difficulty
        }

        return hashMap
    except:
        logging.error("Failed to fetch LeetCode daily question")
        return None


def post_leetcode_question(hMap):
    if not hMap:
        app.client.chat_postMessage(
            channel="leetcode-grind",
            text="LeetCode API decided to ghost me. In that case have a rest guys, we try again tomorrow."
        )
        return
    title = hMap["title"]
    link = hMap["link"]
    difficulty = hMap["difficulty"]
    message = f"""
    
    *Today's LeetCode Question -- {difficulty}*
    {title}
    {link}

                        """
    app.client.chat_postMessage(
    channel="leetcode-grind",
    text=message
    )
    return message
def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
if __name__ == "__main__":
    schedule.every().day.at("10:00").do(lambda: post_leetcode_question(fetch_leetcode_daily()))
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logging.info("⚡️ Bot starting in Socket Mode...")
    try:
        handler = SocketModeHandler(app, app_token)
        logging.info("Socket handler created successfully")
        handler.start()
    except Exception as e:
        logging.error(f"Error starting bot: {e}")