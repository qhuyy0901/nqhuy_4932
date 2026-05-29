from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

# API JSON cho AJAX (
@app.route("/api/caesar/encrypt", methods=['POST'])
def api_caesar_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    shift = int(data.get('shift', 0))
    caesar = CaesarCipher()
    return jsonify({'result': caesar.encrypt_text(text, shift)})

@app.route("/api/caesar/decrypt", methods=['POST'])
def api_caesar_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    shift = int(data.get('shift', 0))
    caesar = CaesarCipher()
    return jsonify({'result': caesar.decrypt_text(text, shift)})


#  ROUTES VIGENERE 
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    encrypted_text = vigenere.encrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    decrypted_text = vigenere.decrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

# API JSON cho Vigenere
@app.route("/api/vigenere/encrypt", methods=['POST'])
def api_vigenere_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    vigenere = VigenereCipher()
    return jsonify({'result': vigenere.encrypt_text(text, key)})

@app.route("/api/vigenere/decrypt", methods=['POST'])
def api_vigenere_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    vigenere = VigenereCipher()
    return jsonify({'result': vigenere.decrypt_text(text, key)})

#  PLAYFAIR 
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.get_json()
    key = data.get('key', '')
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"playfair_matrix": playfair_matrix})

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(text, playfair_matrix)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(text, playfair_matrix)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

# API JSON cho Playfair
@app.route("/api/playfair/encrypt", methods=['POST'])
def api_playfair_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    playfair_cipher = PlayFairCipher()
    matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(text, matrix)
    return jsonify({'result': encrypted_text})

@app.route("/api/playfair/decrypt", methods=['POST'])
def api_playfair_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    key = data.get('key', '')
    playfair_cipher = PlayFairCipher()
    matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(text, matrix)
    return jsonify({'result': decrypted_text})


# RAILFENCE 
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    railfence = RailFenceCipher()
    encrypted_text = railfence.rail_fence_encrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    railfence = RailFenceCipher()
    decrypted_text = railfence.rail_fence_decrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

# API JSON cho Railfence
@app.route("/api/railfence/encrypt", methods=['POST'])
def api_railfence_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    rails = int(data.get('key', data.get('rails', 3)))
    railfence = RailFenceCipher()
    return jsonify({'result': railfence.rail_fence_encrypt(text, rails)})

@app.route("/api/railfence/decrypt", methods=['POST'])
def api_railfence_decrypt():
    data = request.get_json()
    text = data.get('text', '')
    rails = int(data.get('key', data.get('rails', 3)))
    railfence = RailFenceCipher()
    return jsonify({'result': railfence.rail_fence_decrypt(text, rails)})


# ROUTES TRANSPOSITION 
@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])  
    transposition = TranspositionCipher()
    encrypted_text = transposition.encrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/transposition/decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])  
    transposition = TranspositionCipher()
    decrypted_text = transposition.decrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

# API JSON cho Transposition
@app.route("/api/transposition/encrypt", methods=['POST'])
def api_transposition_encrypt():
    data = request.get_json()
    text = data.get('plain_text', data.get('text', ''))
    key = int(data.get('key', 0))
    transposition = TranspositionCipher()
    return jsonify({'result': transposition.encrypt(text, key)})

@app.route("/api/transposition/decrypt", methods=['POST'])
def api_transposition_decrypt():
    data = request.get_json()
    text = data.get('cipher_text', data.get('text', ''))
    key = int(data.get('key', 0))
    transposition = TranspositionCipher()
    return jsonify({'result': transposition.decrypt(text, key)})






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)