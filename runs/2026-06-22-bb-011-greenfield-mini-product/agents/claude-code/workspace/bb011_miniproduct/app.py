from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Scenario(BaseModel):
    id: str
    name: str
    level: int


def create_app() -> FastAPI:
    app = FastAPI()
    store: dict[str, Scenario] = {}

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.post("/scenarios", status_code=201)
    def create(s: Scenario):
        if s.id in store:
            raise HTTPException(status_code=409, detail="duplicate id")
        store[s.id] = s
        return s

    @app.get("/scenarios")
    def list_scenarios():
        return sorted(store.values(), key=lambda x: (x.level, x.id))

    return app
