import os
import azure.functions as func
import datetime
import json
import logging
import requests
from autogen import AssistantAgent

app = func.FunctionApp()



# Step 1: Generate AI DevOps Byte using AutoGen
def generate_ai_byte():

    # Read env values
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
    PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    RECIPIENT = os.getenv("WHATSAPP_RECIPIENT_NUMBER")
    WHATSAPP_API_VERSION = "v18.0"
    WHATSAPP_MAX_LEN = 3500

    agent = AssistantAgent(
        name="EnterpriseAIAgent",
        llm_config={
            "model": "gpt-4o-mini",
            "api_key": OPENAI_KEY
        }
    )

    prompt = f"""
You are a DevOps + AI Tech Intelligence Agent.

Each run, randomly select 2–4 topics from:

• AI + DevOps industry updates
• AI Ethics and Governance
• Agentic AI
• AIOps
• Cloud ecosystem
• Linux OS versions (RHEL, Ubuntu, Debian)
• Kubernetes
• Docker
• Databases (MongoDB, PostgreSQL, Percona)
• Celery
• Angular / React
• Security vulnerabilities & remediation
• OS hardening
• behave / pytest / UI testing
• Programming languages (Go, Rust, Python)
• Important Python library updates

Use realistic current-year technical facts.

Structure:

🚀 Hourly Tech Intelligence Brief

Selected Domains:
(List chosen domains)

Key Updates:
(Concise real-world technical explanation + practical use case.)

Security Insight (if applicable):
(Mention vulnerability type + remediation summary.)

Engineering Impact:
(Why this matters for DevOps/SRE/platform teams.)

--------------------------------------------------

🔧 Sample Commands (add short inline comments)

Example style:
sudo dnf update -y  # Update all RHEL packages
kubectl rollout restart deployment api  # Restart deployment safely
pytest tests/  # Run automated unit tests

Provide 3–6 relevant commands with short comments.

--------------------------------------------------

💻 Code Snippet (add short inline comments)

Provide 5–8 lines relevant snippet.
Each important line must include a short inline comment explaining purpose.

Example style:
from celery import Celery  # Import Celery task queue
app = Celery('tasks', broker='redis://localhost')  # Configure broker

Keep total output under 1700 characters.
Plain text only.
No markdown.
No TERMINATE word.
Rotate domains every run.
Keep comments short and practical.
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    clean_message = str(response).replace("TERMINATE", "").strip()

    return clean_message

# Step 2: Send to WhatsApp
def _get_whatsapp_request_parts(message_text):
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT,
        "type": "text",
        "text": {"body": message_text},
    }
    return url, headers, data


def _post_whatsapp_message(message_text):
    url, headers, data = _get_whatsapp_request_parts(message_text)
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print("Recipient number:", RECIPIENT)
    print("Status:", response.status_code)
    print("Response:", response.text)
    if response.status_code != 200:
        print("❌ WhatsApp API Error Detected")
        print("Error Details:", response.text)
    return response


def send_whatsapp(message_text):
    _post_whatsapp_message(message_text)


def send_whatsapp_long(message_text):
    while len(message_text) > WHATSAPP_MAX_LEN:
        split_index = message_text.rfind("\n", 0, WHATSAPP_MAX_LEN)
        if split_index == -1:
            split_index = WHATSAPP_MAX_LEN

        part = message_text[:split_index]
        send_whatsapp(part)
        message_text = message_text[split_index:].strip()

    send_whatsapp(message_text)

# Main execution
    logging.info("Generating AI DevOps Byte...")
    message = generate_ai_byte()

    logging.info("Generated Message:\n", message)

    logging.info("\nSending this exact message:")
    logging.info("----------------------------")
    logging.info(message)
    logging.info("----------------------------")
    logging.info("Message length:", len(message))
    send_whatsapp_long(message)


@app.timer_trigger(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def hourly_intel_bot(myTimer: func.TimerRequest) -> None:

    message = generate_ai_byte()
    send_whatsapp_long(message)
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
