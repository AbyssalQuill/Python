file_path=r'C:\Users\17367\Desktop\Projects\文本.txt'
try:
    with open(file_path,'r',encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print(f"错误：找不到文件 {file_path}")
except PermissionError:
    print(f"错误：没有权限访问文件 {file_path}")
except Exception as e:
    print(f"读取文件时发生错误：{e}")