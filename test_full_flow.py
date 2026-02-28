from dotenv import load_dotenv
import os
import requests
from autogen import AssistantAgent

# Load environment variables
load_dotenv()

# Read env values
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT = os.getenv("WHATSAPP_RECIPIENT_NUMBER")
WHATSAPP_API_VERSION = "v18.0"
WHATSAPP_MAX_LEN = 3500

# Step 1: Generate AI DevOps Byte using AutoGen
def generate_ai_byte():

    agent = AssistantAgent(
        name="EnterpriseAIAgent",
        llm_config={
            "model": "gpt-4o-mini",
            "api_key": OPENAI_KEY
        }
    )

    prompt = """
Generate a structured enterprise content block with TWO sections.

SECTION 1:
🚀 AI Agent + DevOps Enterprise Case

Industry:
(Choose one: BFSI, Retail, Healthcare, Telecom, Manufacturing)

Customer:
(Realistic enterprise name)

Problem Statement:
(3 lines. Technical + operational challenge.)

AI Agent Architecture:
(Explain multi-agent orchestration – planner, analyzer, remediation agent, monitoring agent.)

Cloud & DevOps Implementation:
(Mention AWS/Azure/GCP, Kubernetes, CI/CD, observability stack.)

Technologies Used:
(List AI libraries, DevOps tools, cloud services.)

Business Impact:
(Include measurable metrics like % cost reduction, % faster deployment.)

Fun Fact:
(Interesting insight about AI in DevOps.)

Python AI Snippet:
(Provide short 5–8 line Python example using openai, autogen, transformers, or langchain.)

--------------------------------------------------

SECTION 2:
🔄 Legacy Modernization Fact

Legacy Stack:
(Randomly choose: LAMP, PHP monolith, AWK-based log parser, KornShell automation script)

Legacy Problem:
(Short description of technical limitation.)

Modernization Approach:
(Explain how it was migrated to microservices, containers, or cloud-native stack.)

Before Snippet (Legacy):
(Provide 3–5 lines workable PHP, AWK, or ksh example.)

After Snippet (Modernized):
(Provide 3–5 lines Python or containerized equivalent.)

Keep total output under 1800 characters.
Ensure complete sentences.
Do not cut words mid-line.
Plain text only.
No markdown.
No TERMINATE word.
Rotate industry and legacy stack randomly.
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
if __name__ == "__main__":
    print("Generating AI DevOps Byte...")
    message = generate_ai_byte()

    print("Generated Message:\n", message)

    print("\nSending this exact message:")
    print("----------------------------")
    print(message)
    print("----------------------------")
    print("Message length:", len(message))
    send_whatsapp_long(message)
