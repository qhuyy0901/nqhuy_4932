
def dao_nguoc_list(lst):
    return lst[::-1]

input_list = input("Nhap danh sach cac so, cach nhau bang dau phap: ")
numbers = list(map(int, input_list.split(',')))

# Sử dụng hàm và in kết quả
list_dao_nguoc = dao_nguoc_list(numbers)
print("List sau khi dao nguoc:", list_dao_nguoc)