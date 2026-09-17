from fastapi import FastAPI
 
app = FastAPI(title="Ytasty Crousty API")
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
