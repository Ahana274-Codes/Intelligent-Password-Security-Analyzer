# src/Train.py
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Import your custom feature engineering steps if applicable
# from Feature_Engineering import your_transformation_function


def run_training_pipeline():
    print("Executing automated training pipeline...")

    # Load your featured dataset
    data_path = os.path.join("Data", "passwords_featured.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing engineered dataset at {data_path}")

    df = pd.read_csv(data_path)

    # --- FIX STEP HERE ---
    # Drop the categorical targets ('label') AND the raw string column (e.g., 'password')
    # Change 'password' to whatever your exact column name is for the raw strings
    X = df.drop(columns=["label", "password"])
    y = df["label"]

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Model Architecture
    # 3. Model Architecture
    model = LogisticRegression(solver="lbfgs", max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    # 4. Export Artifact
    os.makedirs("models", exist_ok=True)
    with open(os.path.join("models", "password_model.pkl"), "wb") as f:
        pickle.dump(model, f)

    print("Pipeline execution complete. Model artifact saved successfully.")


if __name__ == "__main__":
    run_training_pipeline()
