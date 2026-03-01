import datetime
import logging
import os
import feedparser
import requests
from autogen import AssistantAgent

import azure.functions as func


def fetch_latest_headlines():
    feeds = [
        "https://kubernetes.io/feed.xml",
        "https://www.redhat.com/en/rss/blog",
    ]

    headlines = []

    for url in feeds:
        feed = feedparser.parse(url)
        if feed.entries:
            headlines.append(feed.entries[0].title)

    return "\n".join(headlines)


def main(mytimer: func.TimerRequest) -> None:
    logging.info("Tech Intelligence Function Started")

    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
    PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    RECIPIENT = os.getenv("WHATSAPP_RECIPIENT_NUMBER")

    headlines = fetch_latest_headlines()

    agent = AssistantAgent(
        name="AzureTechIntel",
        llm_config={
            "model": "gpt-4o-mini",
            "api_key": OPENAI_KEY
        }
    )

    prompt = f"""
Summarize these headlines into a short DevOps tech brief:

{headlines}

Add 3 sample commands with short comments.
Keep under 1500 characters.
Plain text only.
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    message = str(response).replace("TERMINATE", "").strip()

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)

    logging.info("Message Sent Successfully")