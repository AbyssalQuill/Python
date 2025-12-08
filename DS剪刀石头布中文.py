import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("剪刀石头布")

# 颜色定义
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (86, 156, 214)
BUTTON_HOVER = (129, 184, 223)
RESULT_WIN = (120, 200, 80)
RESULT_LOSE = (224, 108, 117)
RESULT_TIE = (229, 192, 123)
PANEL_COLOR = (58, 63, 73)

# 尝试加载中文字体
try:
    # 尝试使用系统自带的中文字体
    font_large = pygame.font.SysFont("SimHei", 48)
    font_medium = pygame.font.SysFont("SimHei", 36)
    font_small = pygame.font.SysFont("SimHei", 28)
except:
    # 如果失败，使用默认字体
    font_large = pygame.font.SysFont(None, 48)
    font_medium = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 28)

# 游戏选项
CHOICES = ["石头", "布", "剪刀"]
player_choice = None
computer_choice = None
result = None
score = [0, 0, 0]  # [玩家, 电脑, 平局]

# 按钮类
class Button:
    __slots__ = ('rect', 'text', 'action', 'hovered')
    
    def __init__(self, x, y, w, h, text, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

# 游戏逻辑函数
def choose(choice):
    global player_choice, computer_choice, result
    player_choice = choice
    computer_choice = random.choice(CHOICES)
    determine_winner()

def determine_winner():
    global result, score
    if player_choice == computer_choice:
        result = "平局！"
        score[2] += 1
    elif (player_choice == "石头" and computer_choice == "剪刀") or \
         (player_choice == "布" and computer_choice == "石头") or \
         (player_choice == "剪刀" and computer_choice == "布"):
        result = "你赢了！"
        score[0] += 1
    else:
        result = "电脑赢了！"
        score[1] += 1

def reset_game():
    global player_choice, computer_choice, result, score
    player_choice = None
    computer_choice = None
    result = None
    score = [0, 0, 0]

# 创建按钮
buttons = [
    Button(50, 350, 150, 50, "石头", lambda: choose("石头")),
    Button(220, 350, 150, 50, "布", lambda: choose("布")),
    Button(390, 350, 150, 50, "剪刀", lambda: choose("剪刀")),
    Button(220, 420, 150, 50, "重置游戏", reset_game)
]

# 绘制选择图标
def draw_icon(surface, choice, x, y, size=60):
    if choice == "石头":
        pygame.draw.circle(surface, (180, 180, 200), (x, y), size//2, 3)
        pygame.draw.circle(surface, (150, 150, 180), (x, y), size//3, 2)
    elif choice == "布":
        pygame.draw.rect(surface, (200, 230, 200), (x-size//2, y-size//2, size, size), 3, border_radius=10)
        pygame.draw.line(surface, (180, 210, 180), (x-size//2+5, y-size//2+5), (x+size//2-5, y+size//2-5), 2)
    elif choice == "剪刀":
        pygame.draw.line(surface, (230, 200, 200), (x-size//2, y), (x+size//2, y), 3)
        pygame.draw.line(surface, (230, 200, 200), (x, y-size//2), (x, y+size//2), 3)
        pygame.draw.circle(surface, (230, 200, 200), (x, y), size//4, 2)

# 主游戏循环
def main():
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for button in buttons:
                button.check_hover(mouse_pos)
                button.handle_event(event)
        
        # 绘制界面
        screen.fill(BACKGROUND)
        
        # 标题
        title = font_large.render("剪刀石头布游戏", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        # 分数显示
        score_text = font_medium.render(f"玩家: {score[0]}   电脑: {score[1]}   平局: {score[2]}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 70))
        
        # 玩家和电脑选择区域
        pygame.draw.rect(screen, PANEL_COLOR, (50, 120, WIDTH-100, 180), border_radius=15)
        pygame.draw.line(screen, (100, 100, 120), (WIDTH//2, 120), (WIDTH//2, 300), 2)
        
        # 标签
        player_label = font_small.render("你的选择", True, TEXT_COLOR)
        computer_label = font_small.render("电脑选择", True, TEXT_COLOR)
        screen.blit(player_label, (WIDTH//4 - player_label.get_width()//2, 130))
        screen.blit(computer_label, (3*WIDTH//4 - computer_label.get_width()//2, 130))
        
        # 显示选择
        if player_choice:
            draw_icon(screen, player_choice, WIDTH//4, 220)
            choice_text = font_medium.render(player_choice, True, (180, 220, 255))
            screen.blit(choice_text, (WIDTH//4 - choice_text.get_width()//2, 250))
        
        if computer_choice:
            draw_icon(screen, computer_choice, 3*WIDTH//4, 220)
            choice_text = font_medium.render(computer_choice, True, (255, 180, 150))
            screen.blit(choice_text, (3*WIDTH//4 - choice_text.get_width()//2, 250))
        
        # 显示结果
        if result:
            color = RESULT_WIN if result == "你赢了！" else RESULT_LOSE if result == "电脑赢了！" else RESULT_TIE
            result_text = font_large.render(result, True, color)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 300))
        
        # 绘制按钮
        for button in buttons:
            button.draw(screen)
        
        # 游戏规则提示
        rules = font_small.render("石头赢剪刀 | 布赢石头 | 剪刀赢布", True, (180, 180, 180))
        screen.blit(rules, (WIDTH//2 - rules.get_width()//2, 480))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()