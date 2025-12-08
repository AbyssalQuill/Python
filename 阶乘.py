import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
import sys
def calculate_factorial():
    if sys.platform.startswith('win'):
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 启用系统DPI感知
                ctypes.windll.user32.SetProcessDPIAware()  # 兼容旧系统
            except:
                pass
    
    
    
    try:
        n = int(entry.get())
        if n < 0:
            messagebox.showerror("错误", "请输入非负整数")
            return
        
        result = 1
        for i in range(1, n+1):
            result *= i
            
        result_label.config(text=f"{n}! = {result}")
        
        # 添加到历史记录
        history_list.insert(0, f"{n}! = {result}")
        if history_list.size() > 10:
            history_list.delete(10)
            
    except ValueError:
        messagebox.showerror("错误", "请输入有效整数")

# 创建主窗口
root = tk.Tk()
root.title("阶乘计算器")
root.geometry("500x400")
root.resizable(False, False)

# 设置主题
style = ttk.Style()
style.theme_use('clam')

# 创建主框架
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# 标题
title_label = ttk.Label(main_frame, text="阶乘计算器", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# 输入框架
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=20)

ttk.Label(input_frame, text="请输入一个整数:", font=("Arial", 12)).pack(side=tk.LEFT)

entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10)
entry.insert(0, "5")

# 计算按钮
calculate_btn = ttk.Button(main_frame, text="计算阶乘", command=calculate_factorial)
calculate_btn.pack(pady=10)

# 结果显示
result_label = ttk.Label(main_frame, text="结果将显示在这里", font=("Arial", 14, "bold"))
result_label.pack(pady=20)

# 历史记录
history_label = ttk.Label(main_frame, text="历史记录", font=("Arial", 12))
history_label.pack(pady=(30, 10))

history_list = tk.Listbox(main_frame, height=6, font=("Courier", 10))
history_list.pack(fill=tk.BOTH, padx=20)

# 初始计算一次
calculate_factorial()

# 运行主循环
root.mainloop()