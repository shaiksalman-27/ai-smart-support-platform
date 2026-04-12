import os
import requests
from openai import OpenAI

LOCAL_BASE_URL = "http://localhost:8000"

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")


def llm_call(prompt: str) -> str:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN,
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a support assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=60,
    )
    return response.choices[0].message.content or ""


def post_json(url: str, payload: dict) -> dict:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def get_json(url: str) -> dict:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def run_task(task_id: str, actions: list[dict]) -> None:
    reset_result = post_json(
        f"{LOCAL_BASE_URL}/reset",
        {"task_id": task_id},
    )
    print("[STEP]", {"task": task_id, "reset": reset_result})

    for action in actions:
        step_result = post_json(f"{LOCAL_BASE_URL}/step", action)
        print("[STEP]", {"task": task_id, "action": action, "result": step_result})

    state_result = get_json(f"{LOCAL_BASE_URL}/state")
    print("[STEP]", {"task": task_id, "state": state_result})

    grader_result = get_json(f"{LOCAL_BASE_URL}/grader")
    print("[STEP]", {"task": task_id, "grader": grader_result})


def run():
    print("[START]")

    try:
        llm_result = llm_call("Reply in one short sentence: customer support is available.")
        print("[STEP]", {"llm_proxy_response": llm_result})

        run_task(
            "easy_password_reset",
            [
                {"action_type": "classify", "content": "account_access"},
                {"action_type": "set_priority", "content": "low"},
                {"action_type": "resolve", "content": "send_password_reset_steps"},
                {"action_type": "close", "content": ""},
            ],
        )

        run_task(
            "medium_payment_failure",
            [
                {"action_type": "classify", "content": "billing"},
                {"action_type": "set_priority", "content": "high"},
                {"action_type": "ask_info", "content": "Please share your transaction id."},
                {"action_type": "resolve", "content": "request_transaction_id_and_open_billing_review"},
                {"action_type": "close", "content": ""},
            ],
        )

        run_task(
            "hard_account_takeover",
            [
                {"action_type": "classify", "content": "security"},
                {"action_type": "set_priority", "content": "urgent"},
                {"action_type": "ask_info", "content": "Please complete identity verification."},
                {"action_type": "escalate", "content": "security_ops"},
                {"action_type": "close", "content": ""},
            ],
        )

    except Exception as e:
        print("[STEP]", {"error": str(e)})

    print("[END]")


if __name__ == "__main__":
    run()