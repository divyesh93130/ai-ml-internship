"""
unit_conversion.py
Converts frequency units into grams and scales nutrition values
by the requested quantity.
"""

import sqlite3

class UnitConverter:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def to_grams(self, quantity: float, unit: str, food_id: int = None) -> float:
        unit_clean = unit.strip().lower()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if food_id is not None:
            cursor.execute(
                "SELECT grams_equivalent FROM unit_conversions WHERE food_id = ? AND unit = ?",
                (food_id, unit_clean),
            )
            result = cursor.fetchone()
            if result:
                conn.close()
                return quantity * result[0]

        cursor.execute(
            "SELECT grams_equivalent FROM unit_conversions WHERE food_id IS NULL AND unit = ?",
            (unit_clean,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            return quantity * result[0]

        if unit_clean in {"kg", "kilogram", "kilograms"}:
            return quantity * 1000.0
        if unit_clean in {"l", "liter", "litre", "liters", "litres"}:
            return quantity * 1000.0
        if unit_clean in {"ml", "milliliter", "millilitre", "milliliters", "millilitres"}:
            return quantity * 1.0

        return quantity * 1.0


def scale_nutrition(row: dict, grams: float) -> dict:
    factor = grams / 100.0
    nutrient_cols = [
        "calories_kcal",
        "protein_g",
        "carbs_g",
        "fat_g",
        "fiber_g",
        "sugar_g",
        "sodium_mg",
    ]
    result = {
        "food_name": row["food_name"],
        "quantity_grams": round(grams, 1),
    }
    for col in nutrient_cols:
        result[col] = round(float(row.get(col, 0.0)) * factor, 2)
    return result
