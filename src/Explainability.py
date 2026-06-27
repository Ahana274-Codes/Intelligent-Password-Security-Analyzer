import os
import pickle
import pandas as pd


def explain_model_weights():
    model_path = os.path.join("models", "password_model.pkl")
    if not os.path.exists(model_path):
        print("[ERROR] Please train the model first by running src/Train.py")
        return

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("=== 🧠 Model Feature Importance Weights ===")
    # Check if it's a linear model with coefficients
    if hasattr(model, "coef_"):
        features = [
            "length",
            "lowercase_count",
            "uppercase_count",
            "digit_count",
            "special_count",
            "unique_chars",
            "diversity_ratio",
            "entropy",
        ]

        for index, class_label in enumerate(model.classes_):
            print(f"\nTop Drivers for Category: [{class_label.upper()}]")
            coefficients = model.coef_[index]
            for feat, coef in zip(features, coefficients):
                print(f"  -> Feature: {feat:15} | Weight Impact: {coef:.4f}")
    else:
        print("Model architecture does not support raw coefficient extraction.")


if __name__ == "__main__":
    explain_model_weights()
