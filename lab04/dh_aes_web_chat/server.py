"""
Diffie-Hellman + AES Secure Web Chat Server
=============================================
Flow:
1. Server generates DH parameters (p, g as hex) and its own DH key pair
2. When client connects, server sends DH parameters (p_hex, g_hex) + server DH public key (y_hex)
3. Client generates its DH key pair, sends DH public key (y_hex) to server
4. Server relays DH public keys (hex) between clients
5. Each client computes shared secret with every other client using BigInt math
6. AES key is derived from shared secret using HKDF-SHA256 (Web Crypto API)
7. Messages are encrypted with AES-GCM (authenticated encryption)
8. Server CANNOT decrypt messages (true end-to-end encryption)
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dh_aes_secure_chat_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ============================================================
# Generate DH Parameters (p=2048-bit prime, g=2)
# ============================================================
print("[SERVER] Generating DH parameters (2048-bit)... This may take a moment.")
dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
print("[SERVER] DH parameters ready.")

# Extract raw p and g values
dh_pn = dh_parameters.parameter_numbers()
p_hex = format(dh_pn.p, 'x')
g_hex = format(dh_pn.g, 'x')   # Usually "2"

# Generate server's own DH key pair
server_dh_private_key = dh_parameters.generate_private_key()
server_dh_private_numbers = server_dh_private_key.private_numbers()
server_public_key_hex = format(server_dh_private_numbers.public_numbers.y, 'x')

print(f"[SERVER] DH p (first 16 hex): {p_hex[:16]}...")
print(f"[SERVER] Server DH public key (first 16 hex): {server_public_key_hex[:16]}...")

# ============================================================
# Track connected clients: sid -> { dh_public_key_hex, username }
# ============================================================
clients = {}  # { sid: { 'dh_public_key_hex': str, 'username': str } }


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
    # Send DH parameters and server public key as hex
    emit('dh_init', {
        'p_hex': p_hex,
        'g_hex': g_hex,
        'server_dh_public_key_hex': server_public_key_hex
    })


@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    if sid in clients:
        username = clients[sid].get('username', sid[:8])
        del clients[sid]
        print(f"[SERVER] Client disconnected: {username}")
        socketio.emit('system_message', {
            'text': f'🔴 {username} has left the chat',
            'type': 'leave'
        })
        socketio.emit('peer_disconnected', {'sid': sid})
        socketio.emit('client_count', {
            'count': len(clients),
            'clients': [{'sid': s, 'username': v['username']} for s, v in clients.items()]
        })


@socketio.on('client_dh_public_key')
def on_client_dh_public_key(data):
    """
    Client sends its DH public key (hex). Server stores and broadcasts to all peers.
    """
    sid = request.sid
    try:
        client_dh_pub_hex = data['dh_public_key']    # hex string of y = g^a mod p
        username = data.get('username', f'User_{sid[:6]}')

        clients[sid] = {
            'dh_public_key_hex': client_dh_pub_hex,
            'username': username
        }

        print(f"[SERVER] DH public key received from {username} ({sid[:8]}): {client_dh_pub_hex[:16]}...")

        # Acknowledge to sender
        emit('dh_key_accepted', {'message': 'DH key registered successfully'})

        # Broadcast new peer's public key to all OTHER clients
        for other_sid, other_info in list(clients.items()):
            if other_sid != sid:
                # Send new peer's key to existing client
                socketio.emit('new_peer_key', {
                    'sid': sid,
                    'username': username,
                    'dh_public_key': client_dh_pub_hex
                }, to=other_sid)

                # Send existing client's key to new client
                emit('new_peer_key', {
                    'sid': other_sid,
                    'username': other_info['username'],
                    'dh_public_key': other_info['dh_public_key_hex']
                })

        # Notify everyone about new user
        socketio.emit('system_message', {
            'text': f'🟢 {username} joined the chat',
            'type': 'join'
        })
        socketio.emit('client_count', {
            'count': len(clients),
            'clients': [{'sid': s, 'username': v['username']} for s, v in clients.items()]
        })

    except Exception as e:
        print(f"[SERVER] Error in DH key registration: {e}")
        emit('error', {'message': 'DH key registration failed'})


@socketio.on('send_message')
def on_send_message(data):
    """
    Relay encrypted messages. Server CANNOT decrypt them (E2E).
    Each message is encrypted per-recipient with their own DH-derived AES key.
    """
    sid = request.sid
    if sid not in clients:
        emit('error', {'message': 'Not registered'})
        return

    try:
        sender_username = clients[sid]['username']
        recipients = data.get('recipients', {})    # { recipient_sid: encrypted_msg_b64 }
        timestamp = data.get('timestamp', '')

        print(f"[SERVER] Relaying message from {sender_username} to {len(recipients)} recipient(s)")

        for recipient_sid, encrypted_msg in recipients.items():
            if recipient_sid in clients:
                socketio.emit('receive_message', {
                    'sender': sender_username,
                    'sender_sid': sid,
                    'encrypted_message': encrypted_msg,
                    'timestamp': timestamp
                }, to=recipient_sid)

    except Exception as e:
        print(f"[SERVER] Error relaying message: {e}")
        emit('error', {'message': 'Message relay failed'})


if __name__ == '__main__':
    print("[SERVER] Starting DH-AES Secure Chat on http://localhost:5001")
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)
