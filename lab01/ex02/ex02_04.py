
# danh sach rong
j = []
# Duyệt qua tất cả các số trong đoạn từ 2000 đến 3200
for i in range(2000, 3201):     #chia hết cho 7 và kh#ông phải là bội số của 5
    if (i % 7 == 0) and (i % 5 != 0):
        j.append(str(i))        # Thêm số i vào danh sách j
print (','.join(j))
