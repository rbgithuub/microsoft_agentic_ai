import requests
import os

ACCESS_TOKEN = "EAAMopSK0YZCABQyb5Ml0afStnZBe0TZCXzOV90t4ZBvk5FLlsZABlJY5jTB1kS748hgRDKBAu5EhGZAe6Vnxw71myc7ghB6DE6c3IGxAvuqVAlr2uzwZA5khUrr9NGSN8aKDOCJw8IMGjdBRD2GYZBp8cUsFxwJg4JCyR8eaN6OSlIx3yQSVkIQDVGACMUZAwULl52xTMLfJe4JgqmguVWhbd61SZC5wwcg2RZAvIrmwNxeqmtzpfjJ5SL86ejeYImNxIvKGI2UMDhpFafMWGDxhuawnBkqWtws40jG9xYhEQZDZD"
PHONE_NUMBER_ID = "1053322677858335"

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "919962022062",   # your number without +
    "type": "text",
    "text": {
        "body": "🚀 AI DevOps Byte Test Message from AutoGen Bot"
    }
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)