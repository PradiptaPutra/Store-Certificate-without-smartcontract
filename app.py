from flask import Flask, jsonify, request , render_template
from flask_cors import CORS
import base64
import hashlib
import json
import time

app = Flask(__name__, template_folder='templates')
app = Flask(__name__, static_folder='static')

CORS(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
     return render_template('index.html') 


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.proof = 0

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __str__(self):
        return f"Block({self.index}, {self.timestamp}, {self.data}, {self.hash}, {self.proof})"

class Blockchain:
    def __init__(self, difficulty):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def proof_of_work(self):
        block = self.get_latest_block()
        difficulty = self.difficulty
        while True:
            block.proof += 1
            block.hash = block.calculate_hash()
            if block.hash[:difficulty] == "0" * difficulty:
                return block.proof

blockchain = Blockchain(4)

@app.route("/add_cert", methods=["POST"])
def add_cert():
    cert = request.json
    encoded_image = cert["image"]
    image_data = base64.b64decode(encoded_image)
    cert["image"] = hashlib.sha256(image_data).hexdigest()
    proof = blockchain.proof_of_work()
    previous_block = blockchain.get_latest_block()
    cert["previous_hash"] = previous_block.hash
    blockchain.add_block(Block(len(blockchain.chain), time.time(), cert, previous_block.hash))

    return jsonify({
        "message": "Certificate added successfully",
        "proof": proof
    })

@app.route("/view_certificates", methods=["GET"])
def view_certificates():
    certificates = []
    for block in blockchain.chain[1:]:
        certificate = block.data.copy()
        certificate["timestamp"] = block.timestamp
        certificate["previous_hash"] = block.previous_hash
        certificate["proof"] = block.proof
        certificates.append(certificate)
    return jsonify(certificates)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
