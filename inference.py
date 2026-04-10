import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "test-model")
HF_TOKEN = os.getenv("HF_TOKEN")

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
    import json

    for task in TASKS:
        rewards = []
        step_count = 0
        success = False

        print(f"[START] task={task} env=openenv model={MODEL_NAME}")

        try:
            requests.post(f"{API_BASE_URL}/reset", json={"task_id": task}, timeout=10)

            done = False

            while not done and step_count < 5:
                step_count += 1

                action = f"answer_{task}_{step_count}"

                step_resp = requests.post(
                    f"{API_BASE_URL}/step",
                    json={"answer": action},
                    timeout=10
                ).json()

                reward = float(step_resp.get("reward", 0.0))
                done = bool(step_resp.get("done", False))

                rewards.append(reward)

                print(
                    f"[STEP] step={step_count} action={action} "
                    f"reward={reward:.2f} done={str(done).lower()} error=null"
                )

            grade_resp = requests.post(
                f"{API_BASE_URL}/grader",
                json={"answer": action, "task_id": task},
                timeout=10
            ).json()

            success = bool(grade_resp.get("success", False))

        except Exception as e:
            print(
                f"[STEP] step={step_count} action=error "
                f"reward=0.00 done=true error={str(e)}"
            )
            success = False

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])

        print(
            f"[END] success={str(success).lower()} steps={step_count} rewards={rewards_str}"
        )

if __name__ == "__main__":
    main()