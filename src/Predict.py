import os
import pickle
import numpy as np
import pandas as pd
from collections import Counter
import math


class PasswordInferenceEngine:
    """
    Handles live inference requests by loading the serialized model artifact
    and dynamically matching the feature schema from the training dataset.
    """

    def __init__(self, model_relative_path=None, data_relative_path=None):
        if model_relative_path is None:
            model_relative_path = os.path.join("models", "password_model.pkl")
        if data_relative_path is None:
            data_relative_path = os.path.join("Data", "passwords_featured.csv")

        if not os.path.exists(model_relative_path):
            raise FileNotFoundError(
                f"Trained model artifact not found at {model_relative_path}."
            )

        with open(model_relative_path, "rb") as f:
            self.model = pickle.load(f)

        # Dynamically grab the exact column names used during training fit
        if os.path.exists(data_relative_path):
            df_template = pd.read_csv(data_relative_path, nrows=1)
            # Drop target and raw text columns just like in Train.py
            cols_to_drop = [
                col
                for col in ["label", "password", "password_text"]
                if col in df_template.columns
            ]
            self.expected_features = df_template.drop(
                columns=cols_to_drop
            ).columns.tolist()
        else:
            # Fallback to the names verified by scikit-learn's error log
            self.expected_features = [
                "length",
                "lowercase_count",
                "uppercase_count",
                "digit_count",
                "special_count",
                "unique_chars",
                "diversity_ratio",
                "entropy",
            ]

        print(
            "[INFERENCE] Model artifact and feature definitions successfully synchronized."
        )

    def _extract_features(self, password_string):
        """Calculates all possible character metrics dynamically."""
        length = len(password_string)
        lowercase_count = sum(1 for c in password_string if c.islower())
        uppercase_count = sum(1 for c in password_string if c.isupper())
        digit_count = sum(1 for c in password_string if c.isdigit())
        special_count = sum(1 for c in password_string if not c.isalnum())
        unique_chars = len(set(password_string))

        types_present = sum(
            [
                lowercase_count > 0,
                uppercase_count > 0,
                digit_count > 0,
                special_count > 0,
            ]
        )
        diversity_ratio = types_present / 4.0 if length > 0 else 0.0

        if length > 0:
            counts = Counter(password_string)
            entropy = -sum(
                (count / length) * math.log2(count / length)
                for count in counts.values()
            )
        else:
            entropy = 0.0

        # Master mapping dictionary containing all computed statistics
        calculated_metrics = {
            "length": length,
            "lowercase_count": lowercase_count,
            "uppercase_count": uppercase_count,
            "digit_count": digit_count,
            "special_count": special_count,
            "unique_chars": unique_chars,
            "diversity_ratio": diversity_ratio,
            "entropy": entropy,
        }

        # Build the exact dictionary structure ordered exactly how the model expects it
        feature_dict = {}
        for col in self.expected_features:
            # Match columns to calculated values, defaulting to 0 if an unexpected column appears
            feature_dict[col] = [calculated_metrics.get(col, 0)]

        return pd.DataFrame(feature_dict)

    def predict_strength(self, password_string):
        """Runs validation inference on a raw input password string."""
        features_df = self._extract_features(password_string)
        prediction = self.model.predict(features_df)[0]
        return prediction


if __name__ == "__main__":
    engine = PasswordInferenceEngine()

    test_passwords = ["123456", "AhanaArora27", "G00gl3_InTeRn_2027!"]
    print("\n--- System Inference Test Runs ---")
    for pwd in test_passwords:
        result = engine.predict_strength(pwd)
        print(f"Password: {pwd:20} -> Predicted Category: {result}")
