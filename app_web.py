from flask import Flask, request, render_template_string
import time
import hashlib
import json
import socket

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


# Initialize Blockchain
blockchain = Blockchain()

# -------------------------
# HTML Template
# -------------------------
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare Blockchain</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f4; }
        h1, h2 { color: #333; }
        form { background: white; padding: 20px; max-width: 400px; margin-bottom: 30px; border-radius: 8px; }
        input, button { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { background: #4CAF50; color: white; border: none; }
        .block { background: white; padding: 15px; margin-bottom: 15px; border-left: 5px solid #4CAF50;
                 box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 800px; }
        pre { white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <h1>Healthcare Record Blockchain</h1>

    <form action="/add_record" method="post">
        <input type="text" name="patient_id" placeholder="Patient ID" required>
        <input type="text" name="name" placeholder="Patient Name" required>
        <input type="number" name="age" placeholder="Age" required>
        <input type="text" name="disease" placeholder="Disease" required>
        <input type="text" name="treatment" placeholder="Treatment" required>
        <button type="submit">Add Patient Record</button>
    </form>

    <h2>Blockchain</h2>
    {% for block in chain %}
        <div class="block">
            <pre>{{ block | tojson(indent=2) }}</pre>
        </div>
    {% endfor %}
</body>
</html>
'''

# -------------------------
# Flask Routes
# -------------------------
@app.route('/')
def index():
    return render_template_string(template, chain=blockchain.chain)

@app.route('/add_record', methods=['POST'])
def add_record():
    patient_id = request.form['patient_id']
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']
    treatment = request.form['treatment']

    blockchain.add_record(patient_id, name, age, disease, treatment)

    # Mine a block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    blockchain.create_block(proof, previous_hash)

    return render_template_string(template, chain=blockchain.chain)

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    # Get your local IP automatically
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("\n🚀 Flask app is running...")
    print(f"👉 On your computer: http://127.0.0.1:5000")
    print(f"👉 On your phone (same Wi-Fi): http://{local_ip}:5000\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
