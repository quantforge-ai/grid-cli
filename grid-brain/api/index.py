from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

KV_URL = os.environ.get("KV_REST_API_URL")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN")

class ProjectConfig(BaseModel):
    project_id: str
    config: dict

@app.post("/api/register")
def register_project(data: ProjectConfig):
    if not KV_URL:
        raise HTTPException(500, "Brain Damage: KV_URL missing")

    headers = {"Authorization": f"Bearer {KV_TOKEN}"}
    requests.post(f"{KV_URL}/set/{data.project_id}", json=data.config, headers=headers)
    return {"msg": "Project Assimilated."}

@app.get("/api/connect")
def connect_project(project_id: str):
    if not KV_URL:
        raise HTTPException(500, "Brain Damage: KV_URL missing")

    headers = {"Authorization": f"Bearer {KV_TOKEN}"}
    response = requests.get(f"{KV_URL}/get/{project_id}", headers=headers)
    
    data = response.json()
    if data.get("result"):
        return data["result"]
    else:
        raise HTTPException(404, "Project identity not found in memory.")