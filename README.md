# ColorStack SFU Slack Bot

Slack Bot built using GraphQL, Python, Supabase and LeetCode API for automation of various tasks such as LeetCode question postings, community engagement, and Job Scraping

## Implemented Features

- **New Member Welcome**: Automatically sends personalized DM to members when they join a channel.

- **Daily LeetCode Question**: Posts the LeetCode daily challenge to #leetcode-grind every morning at 10 AM with a motivational quote.

- **Error Handling & Logging**: Gracefully handles API failures and logs all events to `bot.log` for debugging

- **Biweekly motivational quote posts to #motivations**: Automated sendding of motivational images to the Slack's dedicated channel, boosting team morale. 

- **Supabase Integration** Uses a custom command to log all solved questions into a PostGreSQL database, allowing for persistence and "immortality" of data. triggered by typing [/leetcode solved Easy|Medium|Hard] after submitting a question to the #leetcode-grind channel

- **LeetCode leaderboard tracking**: Uses custom commands to generate a leaderboard from data previously uploaded to Supabase, triggered by typing [/leetcode leaderboard].

- **Error Handling for invalid and empty commands**: A warm message sent to the user's direct messages whenever an invalid command (like /leetcode fake-command) or an empty command (/leetcode) has been sent.


## Setup

  1. Clone the repository: `git clone https://github.com/Olisaemeka-Paul-Ani/colorstack-sfu-slack-bot.git`
  2. Install dependencies: `pip install -r requirements.txt`
  3. Create a `.env` file with your Slack tokens:
```
   SLACK_BOT_TOKEN=your_bot_token
   SLACK_APP_TOKEN=your_app_token
```
## Tech Stack

- **Python**
- **Slack Bolt SDK**
- **Slack Socket Mode**
- **LeetCode GraphQL API**
- **Python logging module**
- **schedule library (for daily scheduling)**
-**Supabase (for data persistence)**

## Roadmap

- [ ] Job scraping and posting for internship/new grad roles
- [ ] Reaction-based channel interactions
- [ ] AWS EC2 deployment for 24/7 uptime

## Author
   
   **Olisaemeka Paul Ani**  
   [LinkedIn](https://www.linkedin.com/in/olisaemeka-paul-ani/) | [GitHub](https://github.com/Olisaemeka-Paul-Ani)