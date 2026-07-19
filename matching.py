"""
matching.py
The fuzzy food matcher for the Nutrition Analyzer backend.

This module loads food names from SQLite and uses rapidfuzz to match noisy
user input to the best food entry in the database.
"""

import sqlite3
from rapidfuzz import fuzz, process

class FoodMatcher:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._load_food_names()

    def _load_food_names(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT food_name FROM foods ORDER BY food_name")
        rows = cursor.fetchall()
        conn.close()

        self.food_names = [row[0] for row in rows]
        self.food_names_lower = [name.lower() for name in self.food_names]

    def match(self, query: str, top_k: int = 3, score_cutoff: float = 55.0) -> list:
        query_clean = query.strip().lower()
        if not query_clean:
            return []

        results = process.extract(
            query_clean,
            self.food_names_lower,
            scorer=fuzz.WRatio,
            limit=top_k,
            score_cutoff=score_cutoff,
        )

        matches = []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        for matched_name_lower, score, index in results:
            if score < score_cutoff:
                continue
            original_name = self.food_names[index]
            cursor.execute("SELECT * FROM foods WHERE food_name = ?", (original_name,))
            row = cursor.fetchone()
            if row:
                matches.append({
                    "food_name": original_name,
                    "confidence": round(score, 1),
                    "row": dict(row),
                })

        conn.close()
        return matches

    def best_match(self, query: str) -> dict | None:
        matches = self.match(query, top_k=1)
        return matches[0] if matches else None
