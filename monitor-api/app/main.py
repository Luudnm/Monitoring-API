from fastapi import FastAPI, HTTPException
import httpx
import asyncpg
import os

app = FastAPI(title="Kubernetes Service Monitor")

async def check_rest_service():
    """Controleer een interne REST-service via REST_URL variabele."""
    url = os.getenv("REST_URL")
    if not url:
        raise HTTPException(status_code=500, detail="REST_URL not set")
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url)
            ok = resp.status_code == 200 and resp.json().get("status") == "ok"
            status = "healthy" if ok else "unhealthy"
            return {"service": "rest-api", "status": status, "code": resp.status_code}
    except Exception as e:
        return {"service": "rest-api", "status": "unhealthy", "error": str(e)}

async def check_postgres():
    """Controleer PostgreSQL-verbinding."""
    db_host = os.getenv("PG_HOST")
    db_user = os.getenv("PG_USER")
    db_pass = os.getenv("PG_PASS")
    db_name = os.getenv("PG_DB")

    if not all([db_host, db_user, db_pass, db_name]):
        raise HTTPException(status_code=500, detail="DB environment incomplete")

    try:
        conn = await asyncpg.connect(
            host=db_host, user=db_user, password=db_pass, database=db_name
        )
        await conn.execute("SELECT 1;")
        await conn.close()
        return {"service": "postgresql", "status": "healthy"}
    except Exception as e:
        return {"service": "postgresql", "status": "unhealthy", "error": str(e)}

@app.get("/status")
async def get_status():
    rest_status = await check_rest_service()
    pg_status = await check_postgres()
    return {"results": [rest_status, pg_status]}
