from env.tasks import tasks
from env.grader import grade

class OpenEnv:
    def __init__(self):
        self.current_task = None
        self.done = False

    def reset(self, task_id="easy"):
        self.current_task = next(t for t in tasks if t["id"] == task_id)
        self.done = False

        return {
            "query": self.current_task["query"],
            "documents": self.current_task["documents"],
            "step_count": 0
        }

    def step(self, action):
        if self.done:
            return None, 0, True

        answer = action.get("answer", "")
        reference = self.current_task["reference_answer"]

        score = grade(answer, reference)
        reward = score

        self.done = True

        return {"result": answer}, reward, self.done

    def state(self):
        return self.current_task