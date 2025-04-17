import requests
import json
import time
import re

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

model_1 = "llama3"
model_2 = "deepseek-r1"

initial_prompt = input("Enter the starting prompt: ")
turns = int(input("Enter number of turns: "))
current_prompt = initial_prompt

def get_clean_response(model, prompt):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 100  # limit tokens to speed things up
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

    raw_output = ""
    for line in response.iter_lines():
        if line:
            json_data = json.loads(line.decode("utf-8"))
            chunk = json_data.get("response", "")
            raw_output += chunk

    # Remove <think> tags and any content inside them
    cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()

    return cleaned_output

for i in range(turns):
    print(f"\n--- Turn {i + 1} ---")

    print(f"[{model_1}] thinking...")
    reply_1 = get_clean_response(model_1, current_prompt)
    print(f"[{model_1}]: {reply_1}")

    time.sleep(1)

    print(f"\n[{model_2}] thinking...")
    reply_2 = get_clean_response(model_2, reply_1)
    print(f"[{model_2}]: {reply_2}")

    current_prompt = reply_2
    time.sleep(1)
