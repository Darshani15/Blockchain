import streamlit as st
import threading
import time
import hashlib
import json
from flask import Flask, request, jsonify
import requests

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_records = []
        self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'records': self.current_records,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.current_records = []
        self.chain.append(block)
        return block

    def add_record(self, patient_id, name, age, disease, treatment):
        self.current_records.append({
            'patient_id': patient_id,
            'name': name,
            'age': age,
            'disease': disease,
            'treatment': treatment
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# -------------------------
# Flask App Embedded
# -------------------------
flask_app = Flask(__name__)
blockchain = Blockchain()

@flask_app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    patient_id = data.get('patient_id')
    name = data.get('name')
    age = data.get('age')
    disease = data.get('disease')
    treatment = data.get('treatment')

    if not all([patient_id, name, age, disease, treatment]):
        return jsonify({"message": "Missing data"}), 400

    blockchain.add_record(patient_id, name, age, disease, treatment)

    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = hashlib.sha256(json.dumps(blockchain.last_block, sort_keys=True).encode()).hexdigest()
    blockchain.create_block(proof, previous_hash)

    return jsonify({"message": "Record added and block mined!"}), 200

@flask_app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"chain": blockchain.chain}), 200

# -------------------------
# Start Flask in a thread
# -------------------------
def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run_flask, daemon=True).start()
time.sleep(1)  # give Flask time to start

BASE_URL = "http://127.0.0.1:5000"

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Healthcare Blockchain Dashboard", layout="wide")
st.title("🩺 Healthcare Blockchain Dashboard")

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
                st.error(f"❌ Failed to add record. Status code: {res.status_code}")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Could not connect to Flask server inside Streamlit.")

st.subheader("📜 Blockchain Explorer")
try:
    response = requests.get(f"{BASE_URL}/chain", timeout=5)
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
    st.warning("⚠️ Flask server not reachable.")
