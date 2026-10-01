from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from middleware import install_crash_interceptor

app = FastAPI(title="YUGA Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

install_crash_interceptor(app)


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")

ROOMS = {
    "atlas":    {"name": "Atlas Boardroom",   "capacity": 12, "booked": 7},
    "borealis": {"name": "Borealis Hall",     "capacity": 20, "booked": 20},
    "huddle-0": {"name": "Huddle Room",       "capacity": 0,  "booked": 0},
}


class Booking(BaseModel):
    room_id: str
    employee: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "yuga-platform"}


@app.get("/rooms")
def list_rooms():
    return [{"id": k, **v} for k, v in ROOMS.items()]


@app.get("/rooms/{room_id}/occupancy")
def occupancy(room_id: str):
    """
    BUGGY: huddle-0 was provisioned with capacity=0 (bad config row),
    so the occupancy percentage divides by zero.
    """
    r = ROOMS[room_id]
    pct = round(r["booked"] / r["capacity"] * 100) if r["capacity"] > 0 else 0
    return {"room": r["name"], "occupancy_pct": pct}


@app.post("/book")
def book(b: Booking):
    r = ROOMS.get(b.room_id)
    if not r:
        raise HTTPException(404, "room not found")
    if r["booked"] >= r["capacity"]:
        raise HTTPException(409, "room is full")
    r["booked"] += 1
    return {"ok": True, "room": r["name"], "employee": b.employee}


@app.get("/explode")
def explode():
    """
    Demo bug #2: crash message carrying 'platform secrets' — shows
    Presidio scrubbing before data reaches the AI.
    """
    raise RuntimeError(
        "Platform CRM auth failed with api_key=sk-YUGAfake9Key1234567890 "
        "for admin admin@yuga.dev"
    )