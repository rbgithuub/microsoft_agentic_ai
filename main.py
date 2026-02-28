import os
import feedparser
import schedule
import time
from twilio.rest import Client
from autogen import AssistantAgent
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT = os.getenv("WHATSAPP_RECIPIENT_NUMBER")

# Twilio Setup
client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN"))

# RSS Sources
RSS_FEEDS = [
    "https://openai.com/blog/rss.xml",
    "https://aws.amazon.com/blogs/devops/feed/",
    "https://kubernetes.io/feed.xml"
]

def fetch_latest_news():
    news_items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            news_items.append(f"{entry.title}\n{entry.link}")
    return "\n\n".join(news_items)


def generate_short_byte(content):

    agent = AssistantAgent(
        name="TechSummarizer",
        llm_config={
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    )

    prompt = f"""
    Convert the following into a short AI + DevOps technical byte.
    5 lines max.
    Mention why it matters for DevOps or Cloud.

    Content:
    {content}
    """

    response = agent.generate_reply(messages=[{"role": "user", "content": prompt}])
    return response


def send_whatsapp(message_text):

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": "91XXXXXXXXXX",
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    requests.post(url, headers=headers, json=data)

def job():
    print("Fetching news...")
    news = fetch_latest_news()
    short_byte = generate_short_byte(news)
    send_whatsapp(short_byte)
    print("Message sent!")


# Run every hour
schedule.every(1).hours.do(job)

print("AI DevOps WhatsApp Agent Running...")

while True:
    schedule.run_pending()
    time.sleep(10)