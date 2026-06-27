import streamlit as st
import requests

try:
    # 1. THE INSPECTION
    # The code looks up at the browser's address bar to see the website name.
    # If your app is running live, it might see "my-cool-app.streamlit.app".
    current_host = st.context.headers.get("Host", "unknown")

    # 2. YOUR HOME ADDRESS
    # You hardcode your actual, official website URL here.
    # This is the ONLY address that is allowed to run your code.
    my_official_url = "https://intelligent-password-security-analyzer-ewwvyq9fytcnujqjmqrxkn.streamlit.app/"

    # 3. THE SECURITY CHECK
    # The code compares: Is the current website address DIFFERENT from my official address?
    # (We also check 'localhost' so it doesn't trigger alerts while you are developing it at home).
    if my_official_url not in current_host and current_host != "localhost":

        # 4. THE TRAP (Your Webhook Link)
        # If the address doesn't match, it means a thief has copied your code
        # and hosted it on THEIR website. This is your secret tracking link.
        canary_url = " https://webhook.site/7c6235ff-9af5-45e3-93eb-ae77141b2aa4"

        # 5. THE SILENT ALARM
        # The code sends a secret background ping to your Webhook dashboard.
        # It attaches the thief's website name (?unauthorized_domain=...) to the alert.
        requests.get(f"{canary_url}?unauthorized_domain={current_host}", timeout=2)

except:
    # 6. THE ALIBI
    # If anything goes wrong (like no internet or a typo), the code just quits silently.
    # The application keeps running normally so the thief has absolutely no idea they were caught.
    pass

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
    page_title="Intelligent Password Security Analyzer",
    page_icon="🛡️",
    layout="centered",
)

st.title("Intelligent Password Security Analyzer")
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

# This creates an input that triggers a refresh on every single keystroke
user_input = st.text_input(
    "Enter a test password to analyze:", type="password", key="live_input"
)

# This logic runs automatically every time the input changes
# Live Prediction (updates on every keystroke)
status_placeholder = st.empty()

if user_input:
    prediction = engine.predict_strength(user_input)

    prediction = prediction.strip().lower()

    if prediction in ["strong", "high"]:
        status_placeholder.success("🟢 System Status: STRONG Password Tier")

    elif prediction == "medium":
        status_placeholder.warning("🟡 System Status: MEDIUM Password Tier")

    else:
        status_placeholder.error("🔴 System Status: WEAK Password Tier")

else:
    status_placeholder.info("Start typing a password...")

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
