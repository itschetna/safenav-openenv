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
def reset(req: ResetRequest):
    state = env.reset(req.task)

    return {
        "observation": state.dict(),
        "reward": 0.0,
        "done": False,
        "error": None
    }


# ---------------- STEP ----------------
@app.post("/step")
def step(req: StepRequest):
    state, reward, done, error = env.step(req.action)

    return {
        "observation": state.dict(),
        "reward": reward,
        "done": done,
        "error": error
    }