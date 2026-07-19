import os
import sqlite3
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

HERE = Path(__file__).resolve().parent
BASE_DIR = HERE.parent
DATA_DIR = HERE / "data"
DB_PATH = DATA_DIR / "nutrition.db"
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

# Ensure local backend modules are importable when running from the repo root.
sys.path.insert(0, str(HERE))

from matching import FoodMatcher
from unit_conversion import UnitConverter, scale_nutrition

app = FastAPI(title="AI Food Nutrition Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

matcher = None
converter = None

class AnalyzeRequest(BaseModel):
    food_name: str
    quantity: float
    unit: str


def ensure_db_initialized() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT count(*) FROM foods")
            result = cursor.fetchone()
            if result and result[0] > 0:
                return
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()

    from initialize_db import main as initialize_db_main
    initialize_db_main()


@app.on_event("startup")
def startup_event() -> None:
    global matcher, converter
    ensure_db_initialized()
    matcher = FoodMatcher(str(DB_PATH))
    converter = UnitConverter(str(DB_PATH))


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")

    if matcher is None or converter is None:
        raise HTTPException(status_code=500, detail="Backend is not initialized yet.")

    matches = matcher.match(request.food_name, top_k=3)
    if not matches:
        raise HTTPException(status_code=404, detail=f"No close match found for '{request.food_name}'.")

    best = matches[0]
    grams = converter.to_grams(request.quantity, request.unit, food_id=best["row"]["id"])
    nutrition = scale_nutrition(best["row"], grams)

    return {
        "query": {"food_name": request.food_name, "quantity": request.quantity, "unit": request.unit},
        "matched_food": best["food_name"],
        "confidence": best["confidence"],
        "nutrition": nutrition,
        "alternative_matches": [
            {"food_name": item["food_name"], "confidence": item["confidence"]}
            for item in matches[1:]
        ],
    }


if __name__ == "__main__":
    import uvicorn
    ensure_db_initialized()
    matcher = FoodMatcher(str(DB_PATH))
    converter = UnitConverter(str(DB_PATH))
    uvicorn.run("main:app", host="127.0.0.1", port=5500, reload=True)
