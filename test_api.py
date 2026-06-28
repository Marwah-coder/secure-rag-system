import os
from dotenv import load_dotenv
from openai import OpenAI

# .env file se API key load karo
load_dotenv()

# OpenRouter client banao (OpenAI SDK hi use hota hai, bas base_url badal jata hai)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Test request bhejo
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {"role": "user", "content": "Reply in one short sentence: are you working?"}
    ],
)

print("API Response:")
print(response.choices[0].message.content)