from fastapi import FastAPI, Response
app = FastAPI()
@app.get("/health")
async def health():
    return {"status": "ok"
}
