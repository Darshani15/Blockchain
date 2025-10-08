import streamlit as st
import time
import hashlib
import json

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_records = []
        # create the genesis block
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

    @staticmethod
    def hash(block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

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
# Instantiate Blockchain
# -------------------------
blockchain = Blockchain()

# -------------------------
# Streamlit Frontend
# -------------------------
def main():
    st.title("🩺 Healthcare Blockchain System")
    st.markdown("This blockchain securely stores **patient medical records** on-chain.")

    st.subheader(" ➕ Add a New Patient Record")
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    disease = st.text_input("Disease Diagnosed")
    treatment = st.text_input("Treatment Provided")

    if st.button("Add Record & Mine Block"):
        if not all([patient_id.strip(), name.strip(), disease.strip(), treatment.strip()]):
            st.error("⚠️ Please fill in all fields before submitting.")
        else:
            blockchain.add_record(patient_id, name, age, disease, treatment)
            last_proof = blockchain.last_block['proof']
            proof = blockchain.proof_of_work(last_proof)
            prev_hash = blockchain.hash(blockchain.last_block)
            block = blockchain.create_block(proof, prev_hash)
            st.success(f"✅ Block #{block['index']} mined successfully!")
            st.json(block)

    st.markdown("---")
    st.header("⛓️ Current Blockchain")
    for block in blockchain.chain:
        with st.expander(f"Block #{block['index']}"):
            st.json(block)


if __name__ == "__main__":
    main()

