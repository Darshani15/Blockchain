import json
import hashlib
import time
from cryptography.fernet import Fernet
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_records = []

        # Load or generate encryption key
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(self.key)
        self.cipher = Fernet(self.key)

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

        # Backup all records to JSON file
        self.backup_records(block['records'])

        return block

    def add_record(self, patient_id, name, age, disease, treatment):
        record = {
            'patient_id': patient_id,
            'name': name,
            'age': age,
            'disease': disease,
            'treatment': treatment
        }
        # Encrypt record
        encrypted = self.cipher.encrypt(json.dumps(record).encode())
        self.current_records.append(encrypted.decode())
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

    @staticmethod
    def backup_records(records):
        if not records:
            return
        if os.path.exists("records.json"):
            with open("records.json", "r") as f:
                all_records = json.load(f)
        else:
            all_records = []
        all_records.extend(records)
        with open("records.json", "w") as f:
            json.dump(all_records, f, indent=2)
