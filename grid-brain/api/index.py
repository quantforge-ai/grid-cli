from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Vercel automatically injects these
KV_URL = os.environ.get("KV_REST_API_URL")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN")

class ProjectConfig(BaseModel):
    project_id: str
    config: dict

@app.get("/")
def home():
    return {"status": "Grid Brain Online", "mode": "Vercel KV (Redis)"}

@app.post("/api/register")
def register_project(data: ProjectConfig):
    """Lead: Saves config to Redis (Key = Project ID, Value = Config JSON)"""
    if not KV_URL:
        raise HTTPException(500, "Brain Damage: KV_URL missing")

    # Redis command: SET project_id json_string
    # We use the raw REST endpoint provided by Vercel/Upstash
    headers = {"Authorization": f"Bearer {KV_TOKEN}"}
    response = requests.post(
        f"{KV_URL}/set/{data.project_id}", 
        json=data.config,
        headers=headers
    )
    
    if response.status_code == 200:
        return {"msg": "Project Assimilated."}
    else:
        raise HTTPException(500, f"Memory Write Error: {response.text}")

@app.get("/api/connect")
def connect_project(project_id: str):
    """Dev: Gets config from Redis"""
    if not KV_URL:
        raise HTTPException(500, "Brain Damage: KV_URL missing")

    headers = {"Authorization": f"Bearer {KV_TOKEN}"}
    response = requests.get(
        f"{KV_URL}/get/{project_id}",
        headers=headers
    )
    
    data = response.json()
    # Redis REST API returns {"result": "string_value"} or {"result": null}
    
    if data.get("result"):
        # The result comes back as a stringified JSON if we aren't careful, 
        # but usually Vercel KV handles JSON nicely if stored as such. 
        # If it returns a string, the client CLI will parse it.
        return data["result"]
    else:
        raise HTTPException(404, "Project identity not found in memory.")