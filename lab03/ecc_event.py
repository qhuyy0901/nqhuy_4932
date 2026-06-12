import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow

# Địa chỉ API Flask
API_BASE_URL = "http://127.0.0.1:5000/api/ecc"

class ECCWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        """Gắn sự kiện click cho các nút"""
        self.btn_generate.clicked.connect(self.handle_generate)
        self.btn_sign.clicked.connect(self.handle_sign)
        self.btn_verify.clicked.connect(self.handle_verify)

    def handle_generate(self):
        """Nút GENERATE: Tạo cặp khóa ECC"""
        try:
            resp = requests.get(f"{API_BASE_URL}/generate_keys")
            if resp.status_code == 200:
                self.txt_info.setPlainText("Keys generated successfully!")
                self.statusbar.showMessage("Keys generated.", 3000)
            else:
                QMessageBox.warning(self, "API Error", resp.text)
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi kết nối", "Server Flask chưa chạy hoặc sai port!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def handle_sign(self):
        """Nút SIGN: Ký số message"""
        message = self.txt_info.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng nhập message vào ô 'info'!")
            return
            
        try:
            resp = requests.post(f"{API_BASE_URL}/sign", json={"message": message})
            if resp.status_code == 200:
                data = resp.json()
                signature = data.get("signature", "")
                self.txt_sign.setPlainText(f"Signature:\n{signature}")
                self.statusbar.showMessage("Message signed.", 3000)
            else:
                QMessageBox.warning(self, "API Error", resp.text)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def handle_verify(self):
        """Nút VERIFY: Xác minh chữ ký"""
        message = self.txt_info.toPlainText().strip()
        # Lấy signature, loại bỏ dòng tiêu đề nếu có
        raw_sign = self.txt_sign.toPlainText().strip()
        signature = raw_sign.replace("Signature:\n", "").strip()

        if not message or not signature:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Cần có message và signature để verify!")
            return

        try:
            resp = requests.post(f"{API_BASE_URL}/verify", json={
                "message": message,
                "signature": signature
            })
            if resp.status_code == 200:
                is_valid = resp.json().get("valid", False)
                if is_valid:
                    self.txt_sign.setPlainText("VALID - Chữ ký hợp lệ!")
                    self.statusbar.showMessage("Verification successful.", 3000)
                else:
                    self.txt_sign.setPlainText("NVALID - Chữ ký không khớp!")
                    self.statusbar.showMessage("Verification failed.", 3000)
            else:
                QMessageBox.warning(self, "API Error", resp.text)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECCWindow()
    window.show()
    sys.exit(app.exec_())