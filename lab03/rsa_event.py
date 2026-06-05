import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_RSACipher  # ← Sửa: Ui_RSACipher
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RSACipher()  # ← Sửa: Ui_RSACipher
        self.ui.setupUi(self)
        
        # Base URL của Flask API
        self.base_url = "http://127.0.0.1:5000/api/rsa"
        
        # Kết nối các nút với hàm xử lý (SỬA TÊN NÚT)
        self.ui.generateKeysBtn.clicked.connect(self.call_api_gen_keys)
        self.ui.encryptBtn.clicked.connect(self.call_api_encrypt)
        self.ui.decryptBtn.clicked.connect(self.call_api_decrypt)
        self.ui.signBtn.clicked.connect(self.call_api_sign)
        self.ui.verifyBtn.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = f"{self.base_url}/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.setWindowTitle("Success")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def call_api_encrypt(self):
        url = f"{self.base_url}/encrypt"
        payload = {
            "message": self.ui.plainTextEdit.toPlainText(),  # ← Sửa tên
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.cipherTextEdit.setText(data["encrypted_message"])  # ← Sửa tên
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.setWindowTitle("Success")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def call_api_decrypt(self):
        url = f"{self.base_url}/decrypt"
        payload = {
            "ciphertext": self.ui.cipherTextEdit.toPlainText(),  # ← Sửa tên
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.plainTextEdit.setText(data["decrypted_message"])  # ← Sửa tên

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.setWindowTitle("Success")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def call_api_sign(self):
        url = f"{self.base_url}/sign"
        payload = {
            "message": self.ui.infoEdit.toPlainText(),  # ← Sửa tên
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.signatureEdit.setText(data["signature"])  # ← Sửa tên

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.setWindowTitle("Success")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def call_api_verify(self):
        url = f"{self.base_url}/verify"
        payload = {
            "message": self.ui.infoEdit.toPlainText(),  # ← Sửa tên
            "signature": self.ui.signatureEdit.toPlainText()  # ← Sửa tên
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                if data["is_verified"]:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.setWindowTitle("Success")
                else:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Verified Fail")
                    msg.setWindowTitle("Warning")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())