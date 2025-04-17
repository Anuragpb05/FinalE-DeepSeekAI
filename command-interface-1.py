import requests
import json

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

data = {
    "model": "llama3",
    "prompt": "What is water?",
    "stream": False  # Important: disables streaming for easier parsing
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raises error for HTTP problems
    result = response.json()

    print("\nModel Response:")
    print(result["response"].strip())

except requests.exceptions.RequestException as e:
    print("Error communicating with Ollama API:", e)
except (json.JSONDecodeError, KeyError):
    print("Unexpected response format:")
    print(response.text)
