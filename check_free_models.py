import requests

response = requests.get("https://openrouter.ai/api/v1/models")
data = response.json()

print("Free models currently available:\n")
for model in data["data"]:
    pricing = model.get("pricing", {})
    prompt_price = pricing.get("prompt", "1")
    if prompt_price == "0":
        print(model["id"])