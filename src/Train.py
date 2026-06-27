# src/Train.py
import os
import pickle
import random
import string
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from Feature_Engineering import extract_password_features


def generate_synthetic_data():
    """Generates a rich, balanced dataset of 1,500 records to teach the model variance."""
    records = []

    # 1. Generate Weak Passwords (Short, lowercase only, or pure numbers)
    for _ in range(500):
        length = random.randint(4, 7)
        if random.random() > 0.5:
            pwd = "".join(random.choices(string.ascii_lowercase, k=length))
        else:
            pwd = "".join(random.choices(string.digits, k=length))

        features = extract_password_features(pwd)
        features["label"] = "weak"
        records.append(features)

    # 2. Generate Medium Passwords (Medium length, alphanumeric mix)
    for _ in range(500):
        length = random.randint(8, 11)
        chars = string.ascii_letters + string.digits
        pwd = "".join(random.choices(chars, k=length))

        features = extract_password_features(pwd)
        features["label"] = "medium"
        records.append(features)

    # 3. Generate Strong Passwords (Long, mixed-case, numbers, and multiple special symbols)
    specials = "!@#$%^&*()_+=-[]{}|"
    for _ in range(500):
        length = random.randint(13, 18)
        pwd = (
            random.choices(string.ascii_lowercase, k=4)
            + random.choices(string.ascii_uppercase, k=4)
            + random.choices(string.digits, k=4)
            + random.choices(specials, k=4)
        )
        random.shuffle(pwd)
        pwd_str = "".join(pwd)

        features = extract_password_features(pwd_str)
        features["label"] = "strong"
        records.append(features)

    return pd.DataFrame(records)


def run_training_pipeline():
    print("Executing automated training pipeline with synthetic variance generator...")

    # Generate the rich mathematical training dataframe
    df_featured = generate_synthetic_data()

    # Cache the dataset to disk for interviewer review
    os.makedirs("Data", exist_ok=True)
    df_featured.to_csv(os.path.join("Data", "passwords_featured.csv"), index=False)

    # Separate independent and dependent variables
    X = df_featured.drop(columns=["label"])
    y = df_featured["label"]

    # Train/Test Validation Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the model configuration
    model = LogisticRegression(solver="lbfgs", max_iter=2000, random_state=42)
    model.fit(X_train, y_train)

    # Save the updated serialized weights matrix
    os.makedirs("models", exist_ok=True)
    with open(os.path.join("models", "password_model.pkl"), "wb") as f:
        pickle.dump(model, f)

    print(f"Pipeline complete!")
    print(f" -> System Training Set Accuracy: {model.score(X_train, y_train)*100:.2f}%")
    print(f" -> System Testing Set Accuracy: {model.score(X_test, y_test)*100:.2f}%")


if __name__ == "__main__":
    run_training_pipeline()
