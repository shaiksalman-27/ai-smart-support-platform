import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

def run():
    print("[START]")

    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": "Say hello in one short sentence."}
            ],
            "max_tokens": 30,
        }

        response = requests.post(
            f"{API_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )

        print("[STEP]", {
            "status_code": response.status_code,
            "response": response.json()
        })

    except Exception as e:
        print("[STEP]", {"error": str(e)})

    print("[END]")

if __name__ == "__main__":
    run()