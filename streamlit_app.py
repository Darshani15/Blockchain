import streamlit as st
import requests

# Replace with your deployed Flask URL or localhost for testing
BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Healthcare Blockchain", layout="wide")
st.title("🩺 Healthcare Blockchain Dashboard")

# -----------------------------
# Add Record Form
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
            res = requests.post(f"{BASE_URL}/add_record", json=data, timeout=5)
            if res.status_code == 200:
                st.success("✅ Record added and new block mined!")
            else:
                st.error(f"❌ Failed. Status code: {res.status_code}")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Could not connect to Flask server.")

# -----------------------------
# Display Blockchain
# -----------------------------
st.subheader("📜 Blockchain Explorer")
try:
    res = requests.get(f"{BASE_URL}/chain", timeout=5)
    if res.status_code == 200:
        chain = res.json()['chain']
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
        st.error(f"❌ Failed to fetch blockchain. Status: {res.status_code}")
except requests.exceptions.RequestException:
    st.warning("⚠️ Flask server not reachable.")
