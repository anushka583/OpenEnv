from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import OpenEnv
from agents.baseline import baseline_agent
from env.tasks import tasks
from server.app import app

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc"
)
env = OpenEnv()

class GradeRequest(BaseModel):
    answer: str
    task_id: str

@app.get("/")
def home():
    return {"status": "ok", "message": "OpenEnv Research Agent is running"}

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

@app.post("/grader")
def grader(req: GradeRequest):
    env.reset(req.task_id)
    output, score, success = env.step({"answer": req.answer})
    return {
        "result": output["result"],
        "score": score,
        "success": success
    }

@app.post("/reset")
def reset():
    return {"status": "ok"}