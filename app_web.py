from flask import Flask, request, jsonify
import time
import hashlib
import json

app = Flask(__name__)

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_records = []
        self.create_block(proof=100, previous_hash='1')  # Genesis block

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


# Initialize blockchain
blockchain = Blockchain()

# -------------------------
# Flask Routes
# -------------------------
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.form or request.json
    patient_id = data.get('patient_id')
    name = data.get('name')
    age = data.get('age')
    disease = data.get('disease')
    treatment = data.get('treatment')

    if not all([patient_id, name, age, disease, treatment]):
        return jsonify({"message": "Missing data"}), 400

    blockchain.add_record(patient_id, name, age, disease, treatment)

    # Mine a block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    blockchain.create_block(proof, previous_hash)

    return jsonify({"message": "Record added and block mined!"}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"chain": blockchain.chain}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
