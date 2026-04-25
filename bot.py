import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import schedule
import time
import threading
import logging
import random
from supabase import create_client
load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(URL, KEY)

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

def log_solve(user_id,difficulty):
    data = {
        "user_id": user_id,
        "difficulty": difficulty
    }

    supabase.table("solves").insert(data).execute()
    logging.info(f"Recorded Supabase entry for {user_id}")
    return
@app.command("/leetcode")
def handle_command(ack, body, client):
    ack()
    print(body["user_id"])
    print(body["text"])
    log_solve(body["user_id"],body["text"])

MOTIVATIONAL_QUOTES = ["Make it inevitable — one focused rep at a time.",
                      "Ship broken, fix fast, learn faster.",
                      "Debug your fears like you debug your code — line by line.",
                      "Consistency beats intensity every single time.",
                      "Build in public. Fail in public. Grow in public.",
                      "The best time to start was yesterday. The second best is right now.",
                      "You're not behind. You're exactly where you need to be.",
                      "Every expert was once a beginner who refused to quit.",
                      "Don't just solve problems. Build solutions people remember.",
                      "One cannot reap in spring what they do not sow in autumn."]



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
    *Motivational Quote*: {random.choice(MOTIVATIONAL_QUOTES)}
    *Today's LeetCode Question -- {difficulty}*
    {title}
    {link}

                        """
    app.client.chat_postMessage(
    channel="leetcode-grind",
    text=message
    )
    return message





def post_motivational_image():
    image_folder = "assets/motivational_images"
    image_files = os.listdir(image_folder)
    motivation_post = random.choice(image_files)
    motivation_post_path = os.path.join(image_folder, motivation_post)
    app.client.files_upload_v2(
        channel="C0AUHLA18DV",  # Your #motivations channel
        file= motivation_post_path,
        title="Motivational post incoming!!!"
    )
    
    logging.info(f"Sent motivational message to #motivation")
    return


def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":
    schedule.every().monday.at("09:00").do(post_motivational_image)
    schedule.every().thursday.at("09:00").do(post_motivational_image)
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