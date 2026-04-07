from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from my_env.env import SafeNavEnv

app = FastAPI()
env = SafeNavEnv()

# ---------------- REQUEST MODELS ----------------
class ResetRequest(BaseModel):
    task: str = "easy"

class StepRequest(BaseModel):
    action: str

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "SafeNav OpenEnv running"}

# ---------------- RESET ----------------
@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    # Use default task if no body is provided
    task = req.task if req else "easy"
    state = env.reset(task)
    return {
        "observation": state.dict(),
        "reward": 0.0,
        "done": False,
        "error": None
    }

# ---------------- STEP ----------------
@app.post("/step")
def step(req: Optional[StepRequest] = None):
    # Return error if no action provided
    if not req or not req.action:
        return {
            "observation": None,
            "reward": 0.0,
            "done": True,
            "error": "No action provided"
        }
    state, reward, done, error = env.step(req.action)
    return {
        "observation": state.dict(),
        "reward": reward,
        "done": done,
        "error": error
    }
