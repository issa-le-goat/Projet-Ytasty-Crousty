from fastapi import FastAPI
from ytasty_crousty.modules.auths.router import router as auth_router
 
app = FastAPI(title="Ytasty Crousty API")
app.include_router(auth_router)
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
