import random as rd
import time

def write(text, delay=0.1):
    """逐个字符打印文本，实现打字机效果"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # 所有字符显示完后换行

# 游戏欢迎信息
write('欢迎来到投骰子游戏')
time.sleep(1)

# 询问用户是否投骰子（先显示提示，再单独获取输入）
write('是否投骰子：')
choice = input().strip()  # 获取用户输入并去除前后空格

if choice == '是':
    # 只有用户选择投骰子后，才生成双方的点数（修复逻辑顺序问题）
    cpu_choice = rd.randint(1, 6)
    user_choice = rd.randint(1, 6)
    
    time.sleep(1)
    write(f"电脑投掷的结果是：{cpu_choice}")
    time.sleep(1)
    write(f'你投掷的结果是：{user_choice}')
    time.sleep(0.5)
    
    # 判断胜负
    if cpu_choice == user_choice:
        write('平局！')
    elif cpu_choice > user_choice:
        write('电脑获胜！')
    else:
        write('恭喜你获胜！')
else:
    write('下次再玩，再见！')

    

