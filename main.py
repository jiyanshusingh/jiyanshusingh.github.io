#!/usr/bin/env python3
"""
Dynamic portfolio backend — serves the static site + JSON APIs.

Endpoints:
  GET  /                  -> index.html
  GET  /api/projects      -> project list (from projects.json)
  POST /api/contact       -> store a contact message
  GET  /api/visits        -> visitor count (incremented on each page load)
  GET  /health            -> health check
"""
import json
import os
import re
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

ROOT = Path(__file__).resolve().parent
PROJECTS_FILE = ROOT / "projects.json"
DATA_DIR = Path(os.environ.get("DATA_DIR", ROOT))
VISITS_FILE = DATA_DIR / "visits.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"

app = FastAPI(title="Portfolio API", version="2.0.0")


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str = ""
    message: str


def _load_json(path, default):
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return default


def _save_json(path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


@app.get("/health")
def health():
    return {"status": "ok", "app": "portfolio", "version": "2.0.0"}


@app.get("/api/projects")
def get_projects():
    return _load_json(PROJECTS_FILE, [])


@app.post("/api/contact")
async def contact(msg: ContactMessage):
    if not msg.name.strip() or not msg.message.strip():
        return JSONResponse({"ok": False, "error": "Name and message are required"}, status_code=400)
    if len(msg.message) > 5000:
        return JSONResponse({"ok": False, "error": "Message too long"}, status_code=400)
    contacts = _load_json(CONTACTS_FILE, [])
    contacts.append({
        "name": msg.name[:100],
        "email": msg.email,
        "subject": msg.subject[:200],
        "message": msg.message[:5000],
        "ts": time.time(),
    })
    _save_json(CONTACTS_FILE, contacts)
    return {"ok": True, "message": "Message received. Thanks for reaching out!"}


@app.get("/api/visits")
def visits():
    data = _load_json(VISITS_FILE, {"count": 0})
    data["count"] = int(data.get("count", 0)) + 1
    _save_json(VISITS_FILE, data)
    return {"count": data["count"]}


# Static site — serve index.html at / and assets under /assets
app.mount("/assets", StaticFiles(directory=ROOT / "assets"), name="assets")


@app.get("/")
def index():
    return FileResponse(ROOT / "index.html")
