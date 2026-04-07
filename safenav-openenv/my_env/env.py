import json
import os
from typing import Tuple, Optional
from my_env.models import State, Route


class SafeNavEnv:

    def __init__(self):
        self.state: Optional[State] = None
        self.done: bool = False
        self.task: str = "easy"
        self.analyzed: bool = False
        self.max_steps: int = 5

        # ✅ Robust path (works locally + HF)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(base_dir, "data", "routes.json")

    # ---------------- RESET ----------------
    def reset(self, task: str = "easy") -> State:
        self.task = task

        # 🔹 Load dataset safely
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            raise Exception(f"routes.json not found or invalid: {str(e)}")

        # 🔹 Validate task
        if task not in data:
            raise Exception(f"Invalid task: {task}")

        routes_data = data.get(task, [])

        if not routes_data:
            raise Exception(f"No routes found for task: {task}")

        if len(routes_data) < 2:
            raise Exception("Not enough routes for decision")

        # 🔹 Convert JSON → Route objects
        routes = []
        for r in routes_data:
            if not all(k in r for k in ("route_id", "crime_score", "distance")):
                raise Exception("Invalid route format in dataset")

            routes.append(
                Route(
                    route_id=int(r["route_id"]),
                    crime_score=float(r["crime_score"]),
                    distance=float(r["distance"]),
                )
            )

        # 🔹 Initialize state
        self.state = State(
            start="A",
            end="B",
            routes=routes,
            step_count=0,
        )

        self.done = False
        self.analyzed = False

        return self.state

    # ---------------- STEP ----------------
    def step(self, action: str) -> Tuple[State, float, bool, Optional[str]]:
        if self.state is None:
            return None, 0.0, True, "Environment not initialized. Call reset()."

        if self.done:
            return self.state, 0.0, True, "Episode already finished"

        reward = 0.0
        error = None

        # 🔹 increment step
        self.state.step_count += 1

        # 🔹 max step guard
        if self.state.step_count > self.max_steps:
            self.done = True
            return self.state, 0.0, True, "Max steps reached"

        # -------- ACTION: ANALYZE --------
        if action == "analyze":
            if self.analyzed:
                reward = 0.0
            else:
                reward = 0.2
                self.analyzed = True

        # -------- ACTION: CHOOSE ROUTE --------
        elif action.startswith("choose_route_"):
            try:
                route_id = int(action.split("_")[-1])
            except Exception:
                return self.state, -0.1, False, "Invalid action format"

            chosen = next(
                (r for r in self.state.routes if r.route_id == route_id),
                None,
            )

            if not chosen:
                return self.state, -0.1, False, "Invalid route"

            # 🔥 Reward: safety + distance
            try:
                safety = (1.0 - chosen.crime_score) * 0.7
                distance = (1.0 / chosen.distance) * 0.3
                reward = safety + distance
            except Exception:
                reward = 1.0 - chosen.crime_score

            # 🔹 bonus if analyzed
            if self.analyzed:
                reward += 0.1

            reward = min(reward, 1.0)
            self.done = True

        # -------- INVALID ACTION --------
        else:
            reward = -0.1
            error = "Invalid action"

        return self.state, round(reward, 2), self.done, error

    # ---------------- STATE ----------------
    def get_state(self) -> Optional[State]:
        return self.state

    # ---------------- CLOSE (IMPORTANT) ----------------
    def close(self):
        """Optional cleanup for OpenEnv compatibility"""
        self.state = None
        self.done = True