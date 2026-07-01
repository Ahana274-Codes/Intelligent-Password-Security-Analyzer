# 🛡️ Intelligent Password Security Analyzer

A production-grade hybrid security system combining **Machine Learning-based password classification** with a **concurrent breach analysis engine** for scalable credential auditing.

---

## 🏗️ System Architecture & Features

### 🔐 Machine Learning Classification Layer
- Logistic Regression classifier trained on **1,500 balanced synthetic samples**
- Classifies passwords into: `weak`, `medium`, `strong`
- Optimized feature-driven inference pipeline for real-time predictions

---

### 🧠 Dynamic Feature Engineering
Transforms raw passwords into numerical feature vectors using:
- Length-based metrics  
- Character diversity ratios  
- Unique character counts  
- Symbol and digit distribution  
- Structural **Shannon Entropy**

---

### ⚡ Concurrent Breach Analysis Engine
- Multi-threaded batch processing system (`src/Breach_Checker.py`)
- Uses `queue.Queue` for task scheduling
- Implements `threading.Lock` for thread-safe execution
- Enables parallel processing of password batches for scalability

---

### 🌐 Streamlit Web Application
- Interactive dashboard for real-time password analysis
- Supports:
  - Single password prediction
  - Batch password evaluation
- Lightweight, responsive UI for seamless user experience

---

## 📁 Repository Structure

```text
Password-Security-Analyzer/
│
├── app/
│   └── App.py                          # Streamlit UI
│
├── Data/
│   ├── passwords.csv                   # Raw dataset
│   ├── passwords_clean.csv            # Cleaned dataset
│   └── passwords_featured.csv         # Engineered features
│
├── models/
│   ├── password_model.pkl              # Trained ML model
│   └── confusion_matrix.png            # Evaluation output
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_experiments.ipynb
│
├── src/
│   ├── __init__.py
│   ├── Feature_Engineering.py          # Feature extraction pipeline
│   ├── Train.py                        # ML training pipeline
│   ├── Predict.py                      # Inference engine
│   ├── Breach_Checker.py              # Concurrent audit system
│   └── Explainability.py              # Model interpretation module
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md