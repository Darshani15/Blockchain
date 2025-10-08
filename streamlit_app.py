import streamlit as st
import requests

# 🔗 Replace with your deployed Flask URL (HTTPS)
BASE_URL = "https://your-flask-backend-url"  # e.g., https://healthcare-flask.up.railway.app

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
        data = {
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "disease": disease,
            "treatment": treatment
        }
        try:
            res = requests.post(f"{BASE_URL}/add_record", json=data, timeout=10)
            if res.status_code == 200:
                st.success("✅ Record added and new block mined!")
            else:
                st.error(f"❌ Failed to add record. Status code: {res.status_code}")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Could not connect to Flask server. Check the URL.")

# -----------------------------
# Display Blockchain Explorer
# -----------------------------
st.subheader("📜 Blockchain Explorer")
try:
    response = requests.get(f"{BASE_URL}/chain", timeout=10)
    if response.status_code == 200:
        blockchain_data = response.json()
        for block in blockchain_data.get("chain", []):
            st.markdown(f"### Block {block['index']}")
            st.markdown(f"**Timestamp:** {block['timestamp']}")
            st.markdown(f"**Proof:** {block['proof']}")
            st.markdown(f"**Previous Hash:** {block['previous_hash']}")
            st.markdown("**Records:**")
            for record in block["records"]:
                st.json(record)
            st.markdown("---")
    else:
        st.error(f"❌ Could not load blockchain data. Status code: {response.status_code}")
except requests.exceptions.RequestException:
    st.warning("⚠️ Flask server not reachable. Blockchain Explorer offline.")
