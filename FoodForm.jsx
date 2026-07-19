import React, { useState } from "react";
import { analyzeFood } from "../api";
import "./FoodForm.css";

export default function FoodForm({ onResult }) {
  const [foodName, setFoodName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [unit, setUnit] = useState("grams");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");

    if (!foodName.trim() || !quantity || Number(quantity) <= 0) {
      setError("Enter a food name and a quantity greater than 0.");
      return;
    }

    setLoading(true);
    try {
      const data = await analyzeFood({
        food_name: foodName,
        quantity: Number(quantity),
        unit,
      });
      onResult(data);
    } catch (err) {
      setError(err.message);
      onResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1>What did you eat?</h1>
      <p className="sub">Type the food and how much of it — spelling and casual units are fine.</p>

      <div className="row">
        <div className="field">
          <label>Food name</label>
          <input
            type="text"
            placeholder="e.g. Panner Buttr Masala"
            value={foodName}
            onChange={(e) => setFoodName(e.target.value)}
          />
        </div>
      </div>

      <div className="row">
        <div className="field">
          <label>Quantity</label>
          <input
            type="number"
            min="0"
            placeholder="1"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          />
        </div>
        <div className="field">
          <label>Unit</label>
          <select value={unit} onChange={(e) => setUnit(e.target.value)}>
            <option value="grams">grams</option>
            <option value="katori">katori</option>
            <option value="bowl">bowl</option>
            <option value="plate">plate</option>
            <option value="cup">cup</option>
            <option value="piece">piece</option>
            <option value="glass">glass</option>
            <option value="ml">ml</option>
          </select>
        </div>
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze nutrition"}
      </button>

      {error && <div className="error">{error}</div>}
    </div>
  );
}
