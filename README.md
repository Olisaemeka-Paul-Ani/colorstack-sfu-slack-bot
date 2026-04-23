# ColorStack SFU Slack Bot

Slack Bot built using GraphQL, Python and LeetCode API for automation of various tasks such as LeetCode question postings, community engagement, and Job Scraping

## Implemented Features

- **New Member Welcome**: Automatically sends personalized DM to members when they join a channel
- **Daily LeetCode Question**: Posts the LeetCode daily challenge to #leetcode-grind every morning at 10 AM with a motivational quote
- **Error Handling & Logging**: Gracefully handles API failures and logs all events to `bot.log` for debugging


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

## Roadmap

- [ ] LeetCode leaderboard tracking
- [ ] Job scraping and posting for internship/new grad roles
- [ ] Reaction-based channel interactions
- [ ] Daily motivational quote posts to #motivations
- [ ] AWS EC2 deployment for 24/7 uptime

## Author
   
   **Olisaemeka Paul Ani**  
   [LinkedIn](https://www.linkedin.com/in/olisaemeka-paul-ani/) | [GitHub](https://github.com/Olisaemeka-Paul-Ani)