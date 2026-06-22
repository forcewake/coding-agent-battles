from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Scenario(BaseModel):
    id: str
    name: str
    level: int


def create_app() -> FastAPI:
    app = FastAPI()
    scenarios: dict[str, Scenario] = {}

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.post("/scenarios", status_code=201)
    def create_scenario(scenario: Scenario):
        if scenario.id in scenarios:
            raise HTTPException(status_code=409, detail="duplicate id")
        scenarios[scenario.id] = scenario
        return scenario

    @app.get("/scenarios")
    def list_scenarios():
        return sorted(
            (s.model_dump() for s in scenarios.values()),
            key=lambda s: (s["level"], s["id"]),
        )

    return app
