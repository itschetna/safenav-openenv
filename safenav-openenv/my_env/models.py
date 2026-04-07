from pydantic import BaseModel, Field
from typing import List


class Route(BaseModel):
    route_id: int
    crime_score: float = Field(ge=0.0, le=1.0)
    distance: float = Field(gt=0)


class State(BaseModel):
    start: str
    end: str
    routes: List[Route]
    step_count: int


class Action(BaseModel):
    action: str  # e.g., "choose_route_1"