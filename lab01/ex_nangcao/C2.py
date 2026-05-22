import re

s = "100#^sdfkj8902w3ir021@swf-50"  
print(f"Chuỗi: {s}")

numbers = [int(num) for num in re.findall(r'-?\d+', s)]
positive_sum = sum(num for num in numbers if num > 0)
negative_sum = sum(num for num in numbers if num < 0)

print(f"Giá trị dương: {positive_sum}")
print(f"Giá trị âm: {negative_sum}")