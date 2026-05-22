
print("Nhap thong tin nguoi dung (Nhap 'done' de ket thuc):")
line =  []
while True:
    user_input = input()
    if user_input.lower() == 'done':
        break
    line.append(user_input)
    #Chuyển các dòng thành chữ in hoa và in ra màn hình
for i in line:
    print(i.upper())