import streamlit as st
import requests

# -------------------------
# Flask API URL
# -------------------------
BASE_URL = "http://127.0.0.1:5000"  # Or your deployed Flask server

st.set_page_config(page_title="Healthcare Blockchain", layout="wide")
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
            res = requests.post(f"{BASE_URL}/add_record", json=data)
            if res.status_code == 200:
                st.success("✅ Record added successfully and new block mined!")
            else:
                st.error(f"❌ Failed to add record. Status code: {res.status_code}")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Could not connect to Flask server. Make sure it's running.")

# -----------------------------
# Display Blockchain Explorer
# -----------------------------
st.subheader("📜 Blockchain Explorer")
try:
    response = requests.get(f"{BASE_URL}/chain")
    if response.status_code == 200:
        chain = response.json()['chain']
        for block in chain:
            st.markdown(f"### Block {block['index']}")
            st.markdown(f"**Timestamp:** {block['timestamp']}")
            st.markdown(f"**Proof:** {block['proof']}")
            st.markdown(f"**Previous Hash:** {block['previous_hash']}")
            st.markdown("**Records:**")
            for record in block['records']:
                st.json(record)
            st.markdown("---")
    else:
        st.error(f"❌ Could not load blockchain data. Status code: {response.status_code}")
except requests.exceptions.RequestException:
    st.warning("⚠️ Flask server not reachable. Blockchain Explorer offline.")
