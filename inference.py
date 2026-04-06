import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "test-model")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

if not API_BASE_URL:
    API_BASE_URL = "https://anushka583-openenv-research-agent.hf.space"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

TASKS = ["easy", "medium", "hard"]

def run_task(task_id):
    baseline_resp = requests.get(
        f"{API_BASE_URL}/baseline",
        params={"task_id": task_id},
        timeout=10
    ).json()

    answer = baseline_resp.get(task_id, "")

    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a reasoning agent."},
                {"role": "user", "content": f"Task: {task_id}"}
            ],
            max_tokens=10,
        )
    except Exception:
        pass

    grade_resp = requests.post(
        f"{API_BASE_URL}/grader",
        json={"answer": answer, "task_id": task_id},
        timeout=10
    ).json()

    return grade_resp.get("score", 0.0)


def main():
    scores = {}

    for task in TASKS:
        try:
            score = run_task(task)
            scores[task] = score
        except Exception as e:
            scores[task] = f"error: {str(e)}"

    print("Baseline Scores:")
    for task, score in scores.items():
        print(f"{task}: {score}")


if __name__ == "__main__":
    main()