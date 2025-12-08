#冒泡排序
print("冒泡排序：")
a = [5, 3, 8, 2, 1, 4, 7, 6]
for i in range(len(a)):
    for j in range(len(a) - i - 1):
        if a[j] > a[j + 1]:
            a[j], a[j + 1] = a[j + 1], a[j]
print(a)
