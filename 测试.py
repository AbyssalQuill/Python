import random

class Player:
    base_lvl = 1
    base_xp = 0
    base_health = 500
    base_attack = 150
    base_evasion = 10   #基础闪避率
    xp_to_level = 100
    
    def __init__(self, name, is_computer=False):
        self.name = name
        self.lvl = self.base_lvl
        self.xp = self.base_xp
        self.health = self.base_health
        self.attack = self.base_attack
        self.evasion = self.base_evasion  #闪避率
        self.max_health = self.base_health
        self.defense_turns_remaining = 0  #防御剩余回合数
        self.is_computer = is_computer  #标记是否为电脑控制
        
    def 攻击(self, target):
        #检查是否闪避
        if random.randint(1, 100) <= target.evasion:
            print(f"{target.name}成功闪避了{self.name}的攻击！")
            return
            
        damage = random.randint(int(self.attack * 0.8), int(self.attack * 1.2))
        
        #检查是否防御
        if target.defense_turns_remaining > 0:
            reduced_damage = int(damage * 0.5)  #防御减50%伤
            print(f"{target.name}的防御生效，减少了{damage - reduced_damage}点伤害！")
            damage = reduced_damage
        #伤害结算    
        target.health = max(0, target.health - damage)
        print(f"{self.name}对{target.name}用出了猛烈一击，造成了{damage}点伤害！")
        
        if target.health == 0:
            print(f"{target.name}已经被击败！")
            self.gain_xp(50 + target.lvl * 10)  #获经验
            
    def 洞察(self):
        print(f"\n{self.name}的状态：")
        print(f"等级：{self.lvl} | 经验：{self.xp}/{self.xp_to_level}")
        print(f"生命值：{self.health}/{self.max_health} | 攻击力：{self.attack}")
        print(f"闪避率：{self.evasion}%\n")
        
    def 防御(self):
        print(f"{self.name}摆出了防御姿态，准备减少两回合伤害！")
        self.defense_turns_remaining = 2
        
    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name}获得了{amount}点经验！")
        
        #检查是否升级
        while self.xp >= self.xp_to_level:
            self.xp -= self.xp_to_level
            self.lvl += 1
            self.attack += 30
            self.evasion += 2  #增加闪避
            self.max_health += 100
            self.health = self.max_health  #生命回满
            self.xp_to_level = int(self.xp_to_level * 1.5)  #经验增加
            print(f"恭喜{self.name}升级到{self.lvl}级！属性提升了！")

    def computer_choose_action(self):
        if self.health < self.max_health * 0.3:
            #30%生命值以下，有40%概率防御
            if random.random() < 0.4:
                return "3"
        
        #80%概率攻击，20%概率洞察
        if random.random() < 0.8:
            return "1"
        else:
            return "2"

def 回合制战斗(player, computer):
    print("=== 战斗开始！ ===")
    current_player = player
    other_player = computer
    
    while True:
        #检查战斗是否结束
        if player.health <= 0:
            print(f"\n战斗结束！{computer.name}获得了胜利！")
            break
        if computer.health <= 0:
            print(f"\n战斗结束！{player.name}获得了胜利！")
            break
            
        #当前玩家回合
        print(f"\n--- {current_player.name}的回合 ---")
        
        #当前玩家回合开始时，处理防御回合减少
        if current_player.defense_turns_remaining > 0:
            current_player.defense_turns_remaining -= 1
            print(f"{current_player.name}的防御效果还剩{current_player.defense_turns_remaining}回合！")
        
        #根据是否为电脑选择不同的行动方式
        if current_player.is_computer:
            #电脑回合 - 自动选择行动
            choice = current_player.computer_choose_action()
            #显示电脑的选择
            action_map = {"1": "攻击", "2": "洞察", "3": "防御"}
            print(f"{current_player.name}选择了：{action_map[choice]}")
        else:
            #玩家回合 - 手动选择行动
            print("请选择行动：1.攻击 2.洞察 3.防御")
            choice = input("输入数字选择：")
            if choice not in ["1", "2", "3"]:
                print("无效选择，默认进行攻击！")
                choice = "1"
        
        if choice == "1":
            current_player.攻击(other_player)
        elif choice == "2":
            current_player.洞察()
        elif choice == "3":
            current_player.防御()
            
        #交换回合
        current_player, other_player = other_player, current_player

#创建玩家和电脑
player = Player('你的精灵')
computer = Player('野生精灵', is_computer=True)

#开始战斗
回合制战斗(player, computer)

