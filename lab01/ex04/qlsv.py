from sv import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.listSV = []

    def soLuongSinhVien(self):
        return len(self.listSV)

    def themSinhVien(self):
        id = int(input("Nhập ID: "))
        name = input("Nhập tên sinh viên: ")
        gioiTinh = input("Nhập giới tính sinh viên: ")
        nganh = input("Nhập chuyên ngành: ")
        diemTB = float(input("Nhập điểm trung bình: "))
        sv = SinhVien(id, name, gioiTinh, nganh, diemTB)
        self.listSV.append(sv)

    def timSinhVienByID(self, ID):
        for sv in self.listSV:
            if sv.id == ID:
                return sv
        return None

    def updateSinhVien(self, ID):
        sv = self.timSinhVienByID(ID)
        if sv != None:
            name = input("Nhập tên sinh viên: ")
            gioiTinh = input("Nhập giới tính sinh viên: ")
            nganh = input("Nhập chuyên ngành: ")
            diemTB = float(input("Nhập điểm trung bình: "))
            sv.name = name
            sv.gioiTinh = gioiTinh
            sv.nganh = nganh
            sv.diemTB = diemTB
        else:
            print("Không tìm thấy sinh viên có ID:", ID)

    def xoaSinhVien(self, ID):
        sv = self.timSinhVienByID(ID)
        if sv != None:
            self.listSV.remove(sv)
            return True
        return False

    def timSinhVienByName(self, name):
        for sv in self.listSV:
            if sv.name.lower() == name.lower():
                return sv
        return None

    def sortByDiemTB(self):
        self.listSV.sort(key=lambda x: x.diemTB)

    def sortByMajor(self):
        self.listSV.sort(key=lambda x: x.nganh)

    def ShowSinhVien(self, danhSach):
        print(f"{'ID':<5} {'Tên':<20} {'Giới tính':<10} {'Ngành':<15} {'Điểm TB':<10}")
        for sv in danhSach:
            print(f"{sv.id:<5} {sv.name:<20} {sv.gioiTinh:<10} {sv.nganh:<15} {sv.diemTB:<10}")

    def getListSv(self):
        return self.listSV
