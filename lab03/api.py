from flask import Flask, request, jsonify, render_template  # ← Thêm render_template
from cipher.rsa import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher  # ← Import ECC

app = Flask(__name__)

# ================= RSA
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})




@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type']
    private_key, public_key = rsa_cipher.load_keys()
    
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400
    
    encrypted_message = rsa_cipher.encrypt(message, key)
    encrypted_hex = encrypted_message.hex()
    return jsonify({'encrypted_message': encrypted_hex})




@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data['ciphertext']
    key_type = data['key_type']
    private_key, public_key = rsa_cipher.load_keys()
    
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400
    
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)
    return jsonify({'decrypted_message': decrypted_message})



@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})



@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']
    signature = bytes.fromhex(data['signature'])
    _, public_key = rsa_cipher.load_keys()
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})


# ================= ECC
ecc_cipher = ECCCipher()

@app.route("/ecc")
def ecc_page():
    return render_template('ecc.html')  # 

@app.route("/api/ecc/generate_keys", methods=['GET', 'POST'])
def api_ecc_generate_keys():
    ecc_cipher.generate_keys() 
    return jsonify({'message': 'Keys generated successfully'})

@app.route("/api/ecc/sign", methods=['POST'])
def api_ecc_sign():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    result = ecc_cipher.sign_message(message)
    return jsonify(result)

@app.route("/api/ecc/verify", methods=['POST'])
def api_ecc_verify():
    data = request.get_json()
    message = data.get('message', '')
    signature = data.get('signature', '')
    
    if not message or not signature:
        return jsonify({'error': 'Message and signature are required'}), 400
    
    is_valid = ecc_cipher.verify_signature(message, signature)
    return jsonify({'valid': is_valid})


#  MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)