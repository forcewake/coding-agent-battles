from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(authorization: str | None = Header(default=None)):
    # BUG: accidentally accepts every request.
    return True

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.get("/admin")
def admin(_: bool = Depends(require_admin)):
    return {"status": "ok", "scope": "admin"}
