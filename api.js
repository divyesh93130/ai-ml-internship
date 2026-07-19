// api.js
// Single place where the frontend talks to the backend.
// Keeping this separate means if the backend URL changes (e.g. deployed to
// a real server later), you only edit it here.

const API_URL = "/analyze";

export async function analyzeFood({ food_name, quantity, unit }) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ food_name, quantity, unit }),
  });

  const data = await res.json();

  if (!res.ok) {
    // FastAPI sends errors as { detail: "..." }
    throw new Error(data.detail || "Something went wrong");
  }

  return data;
}
