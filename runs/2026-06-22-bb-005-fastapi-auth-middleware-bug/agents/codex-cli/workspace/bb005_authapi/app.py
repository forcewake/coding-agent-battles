from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401)
    if authorization != "Bearer secret-token":
        raise HTTPException(status_code=403)
    return True

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.get("/admin")
def admin(_: bool = Depends(require_admin)):
    return {"status": "ok", "scope": "admin"}
