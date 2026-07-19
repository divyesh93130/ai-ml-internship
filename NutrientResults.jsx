import React from "react";
import "./NutrientResults.css";

export default function NutrientResults({ data }) {
  if (!data) return null;

  const n = data.nutrition;

  return (
    <div className="results">
      <div className="matched">
        Matched to <b>{data.matched_food}</b> for {n.quantity_grams}g
        <span className="confidence">{data.confidence}% match</span>
      </div>

      <div className="grid">
        <div className="nutrient">
          <div className="val">{n.calories_kcal}</div>
          <div className="lbl">Calories (kcal)</div>
        </div>
        <div className="nutrient">
          <div className="val">{n.protein_g}g</div>
          <div className="lbl">Protein</div>
        </div>
        <div className="nutrient">
          <div className="val">{n.carbs_g}g</div>
          <div className="lbl">Carbohydrates</div>
        </div>
        <div className="nutrient">
          <div className="val">{n.fat_g}g</div>
          <div className="lbl">Fat</div>
        </div>
        <div className="nutrient">
          <div className="val">{n.fiber_g}g</div>
          <div className="lbl">Fiber</div>
        </div>
        <div className="nutrient">
          <div className="val">{n.sodium_mg}mg</div>
          <div className="lbl">Sodium</div>
        </div>
      </div>

      {data.alternative_matches.length > 0 && (
        <div className="alts">
          Other possible matches:{" "}
          {data.alternative_matches
            .map((m) => `${m.food_name} (${m.confidence}%)`)
            .join(", ")}
        </div>
      )}
    </div>
  );
}
