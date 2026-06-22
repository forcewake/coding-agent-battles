from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

class Scenario(BaseModel):
    id: str
    name: str
    level: int

def create_app() -> FastAPI:
    app = FastAPI()
    
    # In-memory scenarios database for this app instance
    scenarios: dict[str, Scenario] = {}
    
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}
        
    @app.post("/scenarios", status_code=status.HTTP_201_CREATED)
    def create_scenario(scenario: Scenario):
        if scenario.id in scenarios:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate scenario ID")
        scenarios[scenario.id] = scenario
        return scenario
        
    @app.get("/scenarios")
    def list_scenarios():
        # Returns scenarios sorted by level then id
        return sorted(scenarios.values(), key=lambda s: (s.level, s.id))
        
    return app
