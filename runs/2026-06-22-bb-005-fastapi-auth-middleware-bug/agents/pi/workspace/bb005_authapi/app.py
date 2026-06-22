from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

ADMIN_TOKEN = "Bearer secret-token"

def require_admin(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if authorization != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    return True

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.get("/admin")
def admin(_: bool = Depends(require_admin)):
    return {"status": "ok", "scope": "admin"}
