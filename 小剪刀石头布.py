#剪刀石头布
import random
import time
def typewriter_effect(text, delay=0.1):
    for char in text:
     print(char, end='', flush=True)
     time.sleep(delay)
typewriter_effect("欢迎来到剪刀石头布游戏！", 0.05)
typewriter_effect("你将与电脑进行三局两胜的对决。", 0.05)
typewriter_effect("请输入你的选择：剪刀、石头、布", 0.05)   
choice=['剪刀','石头','布']
user_score=0
computer_score=0    
while user_score<2 and computer_score<2:
    user_choice=input("你的选择是：")
    while user_choice not in choice:
        user_choice=input("无效输入，请重新输入（剪刀、石头、布）：")
    computer_choice=random.choice(choice)
    print(f'电脑选择了：{computer_choice}')
    if user_choice==computer_choice:
        print("平局！")
    elif (user_choice=='剪刀' and computer_choice=='布')\
        or (user_choice=='石头' and computer_choice=='剪刀')\
        or (user_choice=='布' and computer_choice=='石头'):
        print("你赢了这一局！")
        user_score+=1
    else:
        print("电脑赢了这一局！")
        computer_score+=1
        if user_score==2:
            print("恭喜你赢得了比赛！")
        else:
            print("可惜了，电脑赢得了比赛！")
