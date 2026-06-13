"""
AES-RSA Secure Web Chat Server
================================
Flow:
1. Client connects via WebSocket
2. Server sends its RSA Public Key to client
3. Client generates RSA key pair, sends its Public Key to server
4. Server generates a random AES-128 key, encrypts it with client's RSA Public Key
5. Server sends encrypted AES key to client
6. Client decrypts AES key using its RSA Private Key
7. All messages are encrypted/decrypted with AES-CBC
"""

import base64

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aes_rsa_secure_chat_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ============================================================
# Generate Server RSA Key (2048-bit)
# ============================================================
server_key = RSA.generate(2048)
# Export as SPKI DER (base64) for Web Crypto API compatibility
server_public_key_der_b64 = base64.b64encode(
    server_key.publickey().export_key(format='DER')
).decode('utf-8')

print("[SERVER] RSA 2048-bit key pair generated.")

# ============================================================
# Track connected clients: sid -> { aes_key, username }
# ============================================================
clients = {}  # { sid: { 'aes_key': bytes, 'username': str } }


# ============================================================
# AES-CBC Encrypt / Decrypt helpers
# ============================================================
def aes_encrypt(key: bytes, plaintext: str) -> str:
    """Encrypt plaintext string with AES-CBC, return base64 string (iv+ciphertext)."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    raw = cipher.iv + ct_bytes
    return base64.b64encode(raw).decode('utf-8')


def aes_decrypt(key: bytes, b64_data: str) -> str:
    """Decrypt base64 AES-CBC data, return plaintext string."""
    raw = base64.b64decode(b64_data)
    iv = raw[:AES.block_size]
    ct = raw[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')


# ============================================================
# Routes
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')


# ============================================================
# WebSocket Events
# ============================================================
@socketio.on('connect')
def on_connect():
    sid = request.sid
    print(f"[SERVER] Client connected: {sid}")
    # Step 1: Send server's RSA public key (SPKI DER base64) to client
    emit('server_public_key', {'public_key_spki_b64': server_public_key_der_b64})


@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    if sid in clients:
        username = clients[sid].get('username', sid[:8])
        del clients[sid]
        print(f"[SERVER] Client disconnected: {username}")
        # Notify remaining clients
        socketio.emit('system_message', {
            'text': f'🔴 {username} has left the chat',
            'type': 'leave'
        })
        socketio.emit('client_count', {'count': len(clients)})


@socketio.on('client_public_key')
def on_client_public_key(data):
    """
    Client sends its RSA public key.
    Server creates AES key, encrypts it with client's RSA public key, sends back.
    """
    sid = request.sid
    try:
        # Client sends public key as SPKI DER base64 (from Web Crypto API)
        client_pub_key_spki_b64 = data['public_key_spki_b64']
        username = data.get('username', f'User_{sid[:6]}')

        # Import client's RSA public key from SPKI DER
        client_pub_key_der = base64.b64decode(client_pub_key_spki_b64)
        client_pub_key = RSA.import_key(client_pub_key_der)

        # Generate random 32-byte AES-256 key
        aes_key = get_random_bytes(32)

        # Encrypt AES key with client RSA public key using OAEP+SHA256
        cipher_rsa = PKCS1_OAEP.new(client_pub_key, hashAlgo=SHA256)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        encrypted_aes_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')

        # Store client info
        clients[sid] = {
            'aes_key': aes_key,
            'username': username
        }

        print(f"[SERVER] Key exchange complete with {username} ({sid[:8]})")

        # Send encrypted AES key back to client
        emit('aes_key_encrypted', {
            'encrypted_aes_key': encrypted_aes_key_b64,
            'aes_key_preview': aes_key.hex()[:16] + '...'  # for display only
        })

        # Notify all clients about new user
        socketio.emit('system_message', {
            'text': f'🟢 {username} joined the chat',
            'type': 'join'
        })
        socketio.emit('client_count', {'count': len(clients)})

    except Exception as e:
        print(f"[SERVER] Error in key exchange with {sid}: {e}")
        emit('error', {'message': 'Key exchange failed'})


@socketio.on('send_message')
def on_send_message(data):
    """
    Receive encrypted message from client, decrypt it, re-encrypt for each other client.
    """
    sid = request.sid
    if sid not in clients:
        emit('error', {'message': 'Not authenticated'})
        return

    try:
        sender_info = clients[sid]
        sender_aes_key = sender_info['aes_key']
        sender_username = sender_info['username']

        # Decrypt message from sender
        encrypted_msg_b64 = data['encrypted_message']
        plaintext = aes_decrypt(sender_aes_key, encrypted_msg_b64)

        print(f"[SERVER] Message from {sender_username}: {plaintext[:50]}...")

        # === DEMO: broadcast plaintext interception to ALL clients ===
        import datetime
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        socketio.emit('server_intercepted', {
            'sender': sender_username,
            'plaintext': plaintext,
            'encrypted': encrypted_msg_b64[:60] + '...',
            'time': ts
        })

        # Re-encrypt and forward to all OTHER clients
        for other_sid, other_info in clients.items():
            if other_sid != sid:
                other_aes_key = other_info['aes_key']
                re_encrypted = aes_encrypt(other_aes_key, plaintext)
                socketio.emit('receive_message', {
                    'sender': sender_username,
                    'encrypted_message': re_encrypted,
                    'timestamp': data.get('timestamp', '')
                }, to=other_sid)

    except Exception as e:
        print(f"[SERVER] Error forwarding message: {e}")
        emit('error', {'message': 'Message relay failed'})


if __name__ == '__main__':
    print("[SERVER] Starting AES-RSA Secure Chat on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
