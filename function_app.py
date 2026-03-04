import os
import azure.functions as func
import datetime
import json
import logging
import random
import requests
from collections import deque
from autogen import AssistantAgent
from zoneinfo import ZoneInfo


# Read env values
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT = os.getenv("WHATSAPP_RECIPIENT_NUMBER")
WHATSAPP_API_VERSION = "v18.0"
WHATSAPP_MAX_LEN = 3500
conversation_memory = deque(maxlen=5)

app = func.FunctionApp()

IST_TZ = ZoneInfo("Asia/Kolkata")


class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created, IST_TZ)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat(timespec="seconds")


def configure_logging():
    formatter = ISTFormatter(
        "%(asctime)s IST | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        return

    for handler in root_logger.handlers:
        handler.setFormatter(formatter)


configure_logging()


# Step 1: Generate AI DevOps Byte using AutoGen
def generate_ai_byte():
    previous_context = "\n\n".join(conversation_memory)
    topics = [
    "AI + DevOps industry updates",
    "Agentic AI",
    "Linux OS versions",
    "Kubernetes",
    "Docker",
    "Security vulnerabilities",
    "Celery",
    "Databases",
    "Programming languages",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Networks",
    "Artificial Neural Network",
    "Convolutional Neural Network",
    "Recurrent Neural Network",
    "Long Short-Term Memory",
    "Gated Recurrent Unit",
    "Transformer Architecture",
    "Large Language Models",
    "Generative AI",
    "Foundation Models",
    "Prompt Engineering",
    "Fine-tuning",
    "Transfer Learning",
    "Reinforcement Learning",
    "Reinforcement Learning from Human Feedback",
    "Supervised Learning",
    "Unsupervised Learning",
    "Semi-Supervised Learning",
    "Self-Supervised Learning",
    "Federated Learning",
    "Edge AI",
    "AutoML",
    "Explainable AI",
    "Responsible AI",
    "Ethical AI",
    "Model Interpretability",
    "Model Drift",
    "Data Drift",
    "Feature Engineering",
    "Feature Selection",
    "Data Labeling",
    "Data Augmentation",
    "Training Dataset",
    "Validation Dataset",
    "Test Dataset",
    "Hyperparameter Tuning",
    "Cross Validation",
    "Gradient Descent",
    "Stochastic Gradient Descent",
    "Backpropagation",
    "Activation Function",
    "Loss Function",
    "Regularization",
    "Dropout",
    "Batch Normalization",
    "Embeddings",
    "Vector Databases",
    "Retrieval-Augmented Generation",
    "Tokenization",
    "Attention Mechanism",
    "Multi-Head Attention",
    "Positional Encoding",
    "Diffusion Models",
    "Generative Adversarial Networks",
    "Variational Autoencoders",
    "Autoencoders",
    "Knowledge Graphs",
    "Graph Neural Networks",
    "Natural Language Processing",
    "Computer Vision",
    "Speech Recognition",
    "Text-to-Speech",
    "Speech-to-Text",
    "Image Classification",
    "Object Detection",
    "Image Segmentation",
    "Named Entity Recognition",
    "Sentiment Analysis",
    "Topic Modeling",
    "Chatbots",
    "Conversational AI",
    "Multi-modal AI",
    "AI Agents",
    "Autonomous Agents",
    "Multi-Agent Systems",
    "AI Orchestration",
    "Model Serving",
    "Model Deployment",
    "MLOps",
    "LLMOps",
    "Data Pipelines",
    "Feature Store",
    "Experiment Tracking",
    "Model Monitoring",
    "A/B Testing for Models",
    "Synthetic Data",
    "Few-shot Learning",
    "Zero-shot Learning",
    "One-shot Learning",
    "Curriculum Learning",
    "Continual Learning",
    "Meta Learning",
    "Hallucination in AI",
    "Guardrails in AI",
    "Alignment in AI",
    "AI Safety",
    "Artificial General Intelligence"
]
    selected_topic = random.choice(topics)

    enhanced_prompt = f"""
Previous responses:
{previous_context}

Selected topic for this run:
• {selected_topic}

Generate a completely new technical briefing.
Avoid repeating previous themes or explanations from recent responses.
Ensure uniqueness in examples, commands, and code snippets.
"""

    agent = AssistantAgent(
        name="EnterpriseAIAgent",
        llm_config={
            "model": "gpt-4o-mini",
            "api_key": OPENAI_KEY,
            "temperature": 0.9 #increase randomness
        }
    )

    prompt = f"""
You are a DevOps + AI Tech Intelligence Agent.



Each run, use only the selected topic provided below:
• {selected_topic}

Use realistic current-year technical facts.

Every run must:
- Focus on only one selected topic
- Use different commands than previous run
- Use different programming language than previous run
- Change writing style (sometimes concise, sometimes analytical)
- Vary tone slightly
- Keep all sections strictly related to the same selected topic

Structure:

🚀 Hourly Tech Intelligence Brief

Selected Topic:
(Show exactly one selected topic)

Topic Definition:
(Explain the selected topic in simple terms for a non-technical reader.
Include one practical real-life application in Financial, Banking, or Healthcare domain.)

Key Updates:
(Concise real-world technical update related to the selected topic + one practical use case in Financial, Banking, or Healthcare domain.)

Security Insight (if applicable):
(Mention vulnerability type + remediation summary.
If applicable, tie impact to Financial, Banking, or Healthcare systems.)

Engineering Impact:
(Why this matters for DevOps/SRE/platform teams.
Include one practical implementation example in Financial, Banking, or Healthcare domain.)

--------------------------------------------------

🔧 Sample Commands (add short inline comments)

Example style:
sudo dnf update -y  # Update all RHEL packages
kubectl rollout restart deployment api  # Restart deployment safely
pytest tests/  # Run automated unit tests

Provide 3–6 relevant commands with short comments.
Commands must support the same selected topic and be useful for practical implementation.

--------------------------------------------------

💻 Code Snippet (add short inline comments)

Provide 5–8 lines relevant snippet.
Each important line must include a short inline comment explaining purpose.
Code must stay aligned to the same selected topic and a practical Financial/Banking/Healthcare application context.

Example style:
from celery import Celery  # Import Celery task queue
app = Celery('tasks', broker='redis://localhost')  # Configure broker

Keep total output under 1700 characters.
Plain text only.
No markdown.
No TERMINATE word.
Pick only one topic per run. Do NOT repeat topics used in the previous 10 runs.
If a topic was used recently, pick a different topic.
Ensure content is substantially different from previous runs.
Avoid repeating similar explanations.
Keep comments short and practical.
"""
    full_prompt = prompt + enhanced_prompt

    response = agent.generate_reply(
        messages=[{"role": "user", "content": full_prompt}]
    )

    clean_message = str(response).replace("TERMINATE", "").strip()
    conversation_memory.append(clean_message)

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

    logging.info(f"Recipient: {RECIPIENT}")
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Response: {response.text}")
    
    if response.status_code != 200:
        logging.error("WhatsApp API Error Detected")
        logging.error("Error Details: %s", response.text)
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
    


@app.timer_trigger(schedule="0 39 4-14 * * *", arg_name="myTimer")
def hourly_intel_bot(myTimer: func.TimerRequest) -> None:

    try:
      
       logging.info("Generating AI DevOps Byte...")
       message = generate_ai_byte()
       logging.info("Generated Message:\n%s", message)
       logging.info("----------------------------")
       logging.info(message)
       logging.info("----------------------------")
       logging.info("Message length: %s", len(message))
       send_whatsapp_long(message)
       logging.info("Generated Message:\n%s", message)
    
    except Exception as e:
       logging.error(f"ERROR: {str(e)}")
