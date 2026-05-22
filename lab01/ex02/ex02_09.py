
def kiem_tra_so_nguyen_to(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True 
n = int(input("Nhap 1 so: "))
if kiem_tra_so_nguyen_to(n):
    print(n, " la so nguyen to")
else:
    print(n, " khong phai la so nguyen to")