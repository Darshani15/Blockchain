import streamlit as st
import requests
import json

# Flask API base URL
BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Healthcare Blockchain Dashboard", layout="wide")
st.title("🩺 Healthcare Blockchain Dashboard")

# -----------------------------
# Add New Patient Record Form
# -----------------------------
st.subheader("➕ Add Patient Record")
with st.form("add_record_form"):
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    disease = st.text_input("Disease")
    treatment = st.text_input("Treatment")
    submitted = st.form_submit_button("Add Record")

    if submitted:
        try:
            data = {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "disease": disease,
                "treatment": treatment
            }
            res = requests.post(f"{BASE_URL}/add_record", data=data, timeout=5)
            if res.status_code == 200:
                st.success("✅ Record added successfully and new block mined!")
            else:
                st.error(f"❌ Failed to add record. Status code: {res.status_code}")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Could not connect to Flask server. Make sure it's running.")

