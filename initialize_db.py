import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DB_PATH = DATA_DIR / "nutrition.db"
NUTRITION_CSV = DATA_DIR / "nutrition_data.csv"
UNITS_CSV = DATA_DIR / "unit_conversion.csv"


def _read_csv_rows(path: Path):
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader if row and any(str(value).strip() for value in row.values())]


def _create_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT UNIQUE NOT NULL,
            category TEXT,
            calories_kcal REAL,
            protein_g REAL,
            carbs_g REAL,
            fat_g REAL,
            fiber_g REAL,
            sugar_g REAL,
            sodium_mg REAL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS unit_conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER,
            unit TEXT NOT NULL,
            grams_equivalent REAL NOT NULL,
            FOREIGN KEY (food_id) REFERENCES foods(id),
            UNIQUE(food_id, unit)
        )
        """
    )


def _insert_foods(cursor: sqlite3.Cursor, rows: list[dict]) -> None:
    for row in rows:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO foods (
                    food_name, category, calories_kcal, protein_g, carbs_g, fat_g, fiber_g, sugar_g, sodium_mg
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("food_name", "").strip(),
                    row.get("category", "").strip(),
                    float(row.get("calories_kcal", 0) or 0),
                    float(row.get("protein_g", 0) or 0),
                    float(row.get("carbs_g", 0) or 0),
                    float(row.get("fat_g", 0) or 0),
                    float(row.get("fiber_g", 0) or 0),
                    float(row.get("sugar_g", 0) or 0),
                    float(row.get("sodium_mg", 0) or 0),
                ),
            )
        except Exception as exc:
            print(f"Failed to insert food row {row.get('food_name')}: {exc}")


def _insert_generic_conversions(cursor: sqlite3.Cursor, rows: list[dict]) -> None:
    for row in rows:
        unit = str(row.get("unit", "")).strip().lower()
        try:
            grams = float(row.get("grams_equivalent", 0) or 0)
        except ValueError:
            print(f"Skipping invalid unit conversion row: {row}")
            continue

        if not unit or grams <= 0:
            continue

        cursor.execute(
            """
            INSERT OR IGNORE INTO unit_conversions (food_id, unit, grams_equivalent)
            VALUES (NULL, ?, ?)
            """,
            (unit, grams),
        )


def _insert_overrides(cursor: sqlite3.Cursor) -> None:
    overrides = [
        ("Roti", "piece", 40.0),
        ("Chapati", "piece", 40.0),
        ("Samosa", "piece", 120.0),
        ("Banana", "piece", 120.0),
        ("Egg Boiled", "piece", 50.0),
        ("Apple", "piece", 150.0),
        ("Idli", "piece", 50.0),
        ("Dosa", "piece", 80.0),
        ("Gulab Jamun", "piece", 50.0),
        ("Dal Tadka", "katori", 150.0),
        ("Dal Tadka", "bowl", 250.0),
    ]

    for food_name, unit, grams in overrides:
        cursor.execute("SELECT id FROM foods WHERE LOWER(food_name) = ?", (food_name.lower(),))
        row = cursor.fetchone()
        if not row:
            continue
        food_id = row[0]
        cursor.execute(
            """
            INSERT OR REPLACE INTO unit_conversions (food_id, unit, grams_equivalent)
            VALUES (?, ?, ?)
            """,
            (food_id, unit.lower(), grams),
        )


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Creating/updating database at {DB_PATH}...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    _create_tables(cursor)
    conn.commit()

    food_rows = _read_csv_rows(NUTRITION_CSV)
    if food_rows:
        print("Importing food data from nutrition_data.csv...")
        _insert_foods(cursor, food_rows)
        conn.commit()

    conversion_rows = _read_csv_rows(UNITS_CSV)
    if conversion_rows:
        print("Importing generic unit conversions from unit_conversion.csv...")
        _insert_generic_conversions(cursor, conversion_rows)
        conn.commit()

    print("Adding food-specific unit overrides...")
    _insert_overrides(cursor)
    conn.commit()
    conn.close()
    print("Database initialization complete!")


if __name__ == "__main__":
    main()
