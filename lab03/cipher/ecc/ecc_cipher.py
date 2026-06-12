from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature
import os

class ECCCipher:
    def __init__(self, keys_dir='cipher/ecc/keys'):
        self.keys_dir = keys_dir
        os.makedirs(keys_dir, exist_ok=True)
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        """Tạo cặp khóa ECC (curve P-256)"""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        
        # Lưu private key
        with open(f'{self.keys_dir}/private_key.pem', 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Lưu public key
        with open(f'{self.keys_dir}/public_key.pem', 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        return {
            'private_key': self._pem_to_str(f'{self.keys_dir}/private_key.pem'),
            'public_key': self._pem_to_str(f'{self.keys_dir}/public_key.pem')
        }
    
    def load_keys(self):
        """Load khóa từ file"""
        try:
            with open(f'{self.keys_dir}/private_key.pem', 'rb') as f:
                self.private_key = serialization.load_pem_private_key(f.read(), password=None)
            with open(f'{self.keys_dir}/public_key.pem', 'rb') as f:
                self.public_key = serialization.load_pem_public_key(f.read())
            return True
        except:
            return False
    
    def sign_message(self, message: str) -> dict:
        """Ký số thông điệp bằng ECDSA"""
        if not self.private_key:
            self.load_keys()
        
        message_bytes = message.encode('utf-8')
        signature = self.private_key.sign(message_bytes, ec.ECDSA(hashes.SHA256()))
        
        # Encode signature sang hex để dễ truyền
        r, s = decode_dss_signature(signature)
        return {
            'signature': signature.hex(),
            'r': hex(r),
            's': hex(s)
        }
    
    def verify_signature(self, message: str, signature_hex: str) -> bool:
        """Xác minh chữ ký"""
        if not self.public_key:
            self.load_keys()
        
        try:
            signature = bytes.fromhex(signature_hex)
            message_bytes = message.encode('utf-8')
            self.public_key.verify(signature, message_bytes, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
    
    def _pem_to_str(self, filepath: str) -> str:
        with open(filepath, 'r') as f:
            return f.read()