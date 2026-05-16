from qlsv import QuanLySinhVien

qlsv = QuanLySinhVien()
while True:
    print("\nCHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN\n")
    print("================================================")
    print("=  1. Thêm sinh viên                           =")
    print("=  2. Cập nhật thông tin sinh viên bơi ID      =")
    print("=  3. Xóa sinh viên bơi ID                     =")
    print("=  4. Tìm sinh viên theo tên                   =")
    print("=  5. Sắp xếp sinh viên theo điểm trung bình   =")
    print("=  6. Sắp xếp sinh viên theo chuyên ngành      =")
    print("=  7. Hiển thị danh sách sinh viên             =")
    print("=  0. Thoát chương trình                       =")
    print("================================================")
    choice = input("\nNhập lựa chọn của bạn: ")
    if choice == "1":
        qlsv.themSinhVien()
        print("Thêm sinh viên thành công")
    elif choice == "2":
        if(qlsv.soLuongSinhVien() > 0):
            print("\n2. Cập nhật thông tin sinh viên bơi ID")
            id = int(input("Nhập ID sinh viên muốn cập nhập:"))
            qlsv.updateSinhVien(id)
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "3":
        if(qlsv.soLuongSinhVien() > 0):
            print("\n3. Xóa sinh viên bơi ID")
            id = int(input("Nhập ID sinh viên muốn xoá:"))
            if(qlsv.xoaSinhVien(id)):
                print("Xóa thành công sinh viên có ID:",id) 
            else:
                print("Không tìm thấy sinh viên có ID:",id)
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "4":
        if(qlsv.soLuongSinhVien() > 0):
            name = input("Nhập tên sinh viên muốn tìm:")
            sv = qlsv.timSinhVienByName(name)
            if(sv != None):
                print(sv)
            else:
                print("Không tìm thấy sinh viên")
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "5":
        if(qlsv.soLuongSinhVien() >0):
            print("\n5. Sắp xếp sinh viên theo điểm trung bình:")
            qlsv.sortByDiemTB()
            qlsv.ShowSinhVien(qlsv.getListSv())
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "6":
        if(qlsv.soLuongSinhVien() >0):
            print("\n6. Sắp xếp sinh viên theo chuyên ngành:")
            qlsv.sortByMajor()
            qlsv.ShowSinhVien(qlsv.getListSv())
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "7":
        if(qlsv.soLuongSinhVien() >0):
            print("\n7. Hiển thị danh sách sinh viên:")
            qlsv.ShowSinhVien(qlsv.getListSv())
        else:
            print("\nDanh sách sinh viên rỗng")
    elif choice == "0":
        break
    else:
        print("Lựa chọn không hợp lệ")