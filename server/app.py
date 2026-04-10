from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import OpenEnv
from agents.baseline import baseline_agent
from env.tasks import tasks

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc"
)
env = OpenEnv()
current_task = "easy"

class GradeRequest(BaseModel):
    answer: str
    task_id: str

class Action(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"status": "ok", "message": "Openenv Research Agent is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "description": "Extract factual information from a single document",
                "action_schema": {"answer": "string"}
            },
            {
                "id": "medium",
                "description": "Compare and summarize across multiple documents",
                "action_schema": {"answer": "string"}
            },
            {
                "id": "hard",
                "description": "Synthesize insights from multiple sources with trade-offs",
                "action_schema": {"answer": "string"}
            }
        ]
    }

@app.get("/baseline")
def baseline(task_id: str = "easy"):
    state = env.reset(task_id)
    return baseline_agent(state)

@app.post("/reset")
def reset(task_id: str = "easy"):
    global current_task
    current_task = task_id
    state = env.reset(task_id)
    return {"observation": state}

@app.post("/step")
def step(action: Action):
    output, reward, done = env.step({"answer": action.answer})
    return {
        "observation": output,
        "reward": float(reward),
        "done": bool(done),
        "info": {}
    }

@app.get("/state")
def state():
    return {
        "task": current_task,
        "status": "running"
    }

@app.post("/grader")
def grader(req: GradeRequest):
    env.reset(req.task_id)
    output, score, success = env.step({"answer": req.answer})
    return {
        "result": output.get("result", ""),
        "score": float(score),
        "success": bool(success)
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()