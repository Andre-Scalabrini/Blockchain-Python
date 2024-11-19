from flask import Flask, request, jsonify, Response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'blockchain')))

from blockchain import Blockchain
import logging


app = Flask(__name__, static_folder='../frontend')


# Instância da blockchain
blockchain = Blockchain()

# Configuração de logs
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(filename="logs/audit.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.after_request
def add_csp(response: Response):
    # Adicionando o cabeçalho CSP para permitir scripts locais
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline' 'unsafe-eval'; object-src 'none';"
    return response

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

# Rota para servir arquivos estáticos (CSS, JS, etc.)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route("/register", methods=["POST"])
def register():
    data = request.json.get("data")
    if not data:
        return jsonify({"error": "Data is required"}), 400
    new_block = blockchain.add_block(data)
    logging.info(f"Data registered: {data}")
    return jsonify({"message": "Block added", "block": new_block.to_dict()}), 201

@app.route("/blocks", methods=["GET"])
def get_blocks():
    return jsonify(blockchain.to_dict()), 200

@app.route("/audit", methods=["GET"])
def audit_chain():
    is_valid = blockchain.is_chain_valid()
    logging.info(f"Blockchain audit performed: Valid = {is_valid}")
    return jsonify({"is_valid": is_valid}), 200

@app.route("/register_peer", methods=["POST"])
def register_peer():
    peer = request.json.get("peer")
    if not peer:
        return jsonify({"error": "Peer address is required"}), 400
    blockchain.register_peer(peer)
    return jsonify({"message": "Peer registered successfully"}), 200

@app.route("/synchronize", methods=["GET"])
def synchronize():
    blockchain.synchronize()
    return jsonify({"message": "Blockchain synchronized", "chain": blockchain.to_dict()}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)