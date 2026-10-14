"""POIBenchWeb backend: computation API + static frontend."""
import math
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="POIBenchWeb")
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


class PointPair(BaseModel):
    ref_lat: float = Field(ge=-90, le=90)
    ref_lon: float = Field(ge=-180, le=180)
    cmp_lat: float = Field(ge=-90, le=90)
    cmp_lon: float = Field(ge=-180, le=180)
    threshold_m: float = Field(default=1000, gt=0)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    r = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/distance")
def distance(pair: PointPair):
    d = haversine_m(pair.ref_lat, pair.ref_lon, pair.cmp_lat, pair.cmp_lon)
    return {
        "distance_m": round(d, 1),
        "threshold_m": pair.threshold_m,
        "is_candidate": d <= pair.threshold_m,
    }


# Serve frontend at "/" (must be mounted after API routes)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
