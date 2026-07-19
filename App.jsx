import React, { useState } from "react";
import FoodForm from "./components/FoodForm";
import NutrientResults from "./components/NutrientResults";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      <FoodForm onResult={setResult} />
      <NutrientResults data={result} />
    </div>
  );
}
