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
# Initialize Blockchain
# -------------------------
blockchain = Blockchain()

# -------------------------
# Flask Routes
# -------------------------
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    required_fields = ["patient_id", "name", "age", "disease", "treatment"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    blockchain.add_record(
        data["patient_id"],
        data["name"],
        data["age"],
        data["disease"],
        data["treatment"]
    )

    # Mine a new block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = hashlib.sha256(json.dumps(blockchain.last_block, sort_keys=True).encode()).hexdigest()
    block = blockchain.create_block(proof, previous_hash)

    return jsonify({"message": "Record added and block mined", "block": block}), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"chain": blockchain.chain}), 200


# -------------------------
# Run Flask
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
