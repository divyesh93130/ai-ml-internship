"""
assignment-1.py

Simple ML assignment script for the ai-ml-internship repository.

What it does:
- Loads the Iris dataset from scikit-learn
- Splits into train/test sets
- Standardizes features
- Trains a Logistic Regression classifier
- Evaluates accuracy on the test set
- Saves the trained model to disk (optional path)

Usage:
    python assignment-1.py --save-model ./assignment1_model.joblib

Dependencies:
    scikit-learn
    joblib (optional - scikit-learn includes joblib functionality)

Install dependencies:
    pip install scikit-learn joblib

"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline(random_state: int = 42) -> Pipeline:
    """Builds and returns an sklearn Pipeline with scaling + logistic regression."""
    clf = LogisticRegression(random_state=random_state, max_iter=200)
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", clf),
        ]
    )
    return pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assignment 1: train a simple classifier on Iris dataset")
    parser.add_argument("--test-size", type=float, default=0.2, help="fraction of data to use as test set")
    parser.add_argument("--random-state", type=int, default=42, help="random seed for reproducibility")
    parser.add_argument("--save-model", type=str, default="assignment1_model.joblib", help="path to save trained model")
    parser.add_argument("--no-save", action="store_true", help="do not save the trained model to disk")
    args = parser.parse_args(argv)

    # Load data
    data = load_iris()
    X = data.data
    y = data.target

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state, stratify=y
    )

    # Build pipeline and train
    pipeline = build_pipeline(random_state=args.random_state)
    pipeline.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {acc:.4f}")
    print("Classification report:")
    print(classification_report(y_test, y_pred, target_names=data.target_names))

    # Save model
    if not args.no_save:
        save_path = Path(args.save_model)
        save_dir = save_path.parent
        if save_dir and not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, save_path)
        print(f"Saved trained model to: {save_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
