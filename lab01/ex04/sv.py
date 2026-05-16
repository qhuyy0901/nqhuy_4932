class SinhVien:
    def __init__(self, id, name, gioiTinh, nganh, diemTB):
        self.id = id
        self.name = name
        self.gioiTinh = gioiTinh
        self.nganh = nganh
        self.diemTB = diemTB

    def __str__(self):
        return f"ID: {self.id}, Tên: {self.name}, Giới tính: {self.gioiTinh}, Ngành: {self.nganh}, Điểm TB: {self.diemTB}"
