from fastapi import FastAPI

app = FastAPI()

@app.get("/baseline")
def baseline(task_id: str):
    return {task_id: "sample answer"}

@app.post("/grader")
def grader(data: dict):
    return {"score": 1.0}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()