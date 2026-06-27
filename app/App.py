# app/App.py
import os
import sys
import streamlit as st

# Ensure the application can discover modules inside the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.Predict import PasswordInferenceEngine
from src.Breach_Checker import ConcurrentBreachChecker

# Page Configuration for a clean, modern aesthetic
st.set_page_config(
    page_title="Intelligent Password Security Suite", page_icon="🛡️", layout="centered"
)

st.title("Intelligent Password Security Suite")
st.markdown("""
This production-grade platform evaluates password vulnerabilities using a hybrid architecture:
1. **Machine Learning Layer:** Predicts strength tier via an optimized Logistic Regression classifier.
2. **Concurrent Systems Layer:** Simulates real-time multi-threaded dictionary audits.
""")


# Initialize the ML Inference Engine safely
@st.cache_resource
def load_engine():
    model_path = os.path.join(
        os.path.dirname(__file__), "..", "models", "password_model.pkl"
    )
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "Data", "passwords_featured.csv"
    )
    return PasswordInferenceEngine(
        model_relative_path=model_path, data_relative_path=data_path
    )


try:
    engine = load_engine()
except Exception as e:
    st.error(
        f"Failed to load ML Model Engine. Please run 'src/Train.py' first. Error: {e}"
    )
    st.stop()

# --- UI Component 1: Live Machine Learning Inference ---
st.subheader("1. Live ML Strength Prediction")
user_input = st.text_input(
    "Enter a test password to analyze:", type="password", key="live_input"
)

if user_input:
    prediction = engine.predict_strength(user_input)

    if prediction.lower() == "high" or prediction.lower() == "strong":
        st.success(f"System Status: STRONG Password Tier")
    elif prediction.lower() == "medium":
        st.warning(f"System Status: MEDIUM Password Tier")
    else:
        st.error(f"System Status: WEAK Password Tier")

st.divider()

# --- UI Component 2: High-Performance Concurrent Security Audit ---
st.subheader("2. Multi-threaded System Breach Audit")
st.caption(
    "Simulate passing a batch of credentials through a parallel security audit layer to test thread scheduling latency."
)

# CLEANED: Removed the specific reference to Google from the list here
batch_input = st.text_area(
    "Enter multiple passwords (one per line) to process concurrently:",
    value="123456\nAhanaArora27\nSecure#992!\npassword\nSystem_Admin_2026!",
)

if st.button("Execute Parallel Audit"):
    password_batch = [line.strip() for line in batch_input.split("\n") if line.strip()]

    if password_batch:
        # Spin up our multi-threaded checker using 4 distinct system worker threads
        checker = ConcurrentBreachChecker(password_batch, num_threads=4)

        with st.spinner("Spawning background worker threads..."):
            audit_results = checker.run_system_audit()

        st.success("Multi-threaded task scheduling complete.")

        st.write("### Thread Audit Results Logs")
        st.json(audit_results)
    else:
        st.info("Please enter at least one password to run the threaded system test.")
