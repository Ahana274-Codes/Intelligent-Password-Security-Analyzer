# 🛡️ Intelligent Password Security Analyzer

A production-grade, hybrid security application combining statistical Machine Learning inference with a high-performance concurrent breach analysis engine.

## 🏗️ System Architecture & Features
- **Machine Learning Classification Layer:** Utilizes an optimized Logistic Regression classifier trained across 1,500 balanced synthetic samples to evaluate passwords into strict `weak`, `medium`, and `strong` security tiers.
- **Dynamic Feature Extraction:** Computes mathematical vector metadata from raw text inputs (including length, distinct subset counts, character class diversity indexes, and structural **Shannon Entropy**) at runtime.
- **Concurrent Systems Engineering:** Implements a multi-threaded batch auditor in `src/Breach_Checker.py` using thread-safe structures (`queue.Queue`) and explicit synchronization routines (`threading.Lock`) to execute parallel credential compliance audits.
- **UX Dashboard Frontend:** Integrates an interactive web interface powered by **Streamlit** to handle single live classifications and bulk multi-threaded operations seamlessly.

## 📁 Repository Structural Design
```text
Password-Security-Analyzer/
├── app/
│   └── App.py                 # Streamlit UI Interface
├── Data/
│   ├── passwords.csv          # Base Raw Input Sets
│   └── passwords_featured.csv # Extracted Statistical Matrices
├── models/
│   └── password_model.pkl     # Serialized Model Weights Artifact
├── notebooks/
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb   # Plotting Confusion Metrics
│   └── 06_experiments.ipynb        # Hyperparameter Registry Log
└── src/
    ├── Feature_Engineering.py # Vector Extraction Logic
    ├── Train.py               # Dataset Generation & ML Pipeline Pipeline
    ├── Predict.py             # Active Inference Driver
    ├── Breach_Checker.py      # Concurrent Thread Task Processor
    └── Explainability.py      # Coefficient Diagnostics Weight Module
