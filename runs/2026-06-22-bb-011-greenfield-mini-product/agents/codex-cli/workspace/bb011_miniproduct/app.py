from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class Scenario(BaseModel):
    id: str
    name: str
    level: int


def create_app():
    app = FastAPI()
    scenarios: dict[str, Scenario] = {}

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.post("/scenarios", status_code=status.HTTP_201_CREATED)
    def create_scenario(scenario: Scenario):
        if scenario.id in scenarios:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="duplicate id")
        scenarios[scenario.id] = scenario
        return scenario

    @app.get("/scenarios")
    def list_scenarios():
        return sorted(scenarios.values(), key=lambda scenario: (scenario.level, scenario.id))

    return app
