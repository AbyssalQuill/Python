import random
import sys
from ctypes import windll  # DPI

import pygame

windll.shcore.SetProcessDpiAwareness(1)
    


# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# 颜色定义
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (86, 156, 214)
BUTTON_HOVER = (129, 184, 223)
RESULT_WIN = (120, 200, 80)
RESULT_LOSE = (224, 108, 117)
RESULT_TIE = (229, 192, 123)
PANEL_COLOR = (58, 63, 73)

# 字体
font_large = pygame.font.SysFont(None, 48)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 28)

# 游戏选项
CHOICES = ["ROCK", "PAPER", "SCISSORS"]
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
        result = "TIE!"
        score[2] += 1
    elif (player_choice == "ROCK" and computer_choice == "SCISSORS") or \
         (player_choice == "PAPER" and computer_choice == "ROCK") or \
         (player_choice == "SCISSORS" and computer_choice == "PAPER"):
        result = "YOU WIN!"
        score[0] += 1
    else:
        result = "COMPUTER WINS!"
        score[1] += 1

def reset_game():
    global player_choice, computer_choice, result, score
    player_choice = None
    computer_choice = None
    result = None
    score = [0, 0, 0]

# 创建按钮
buttons = [
    Button(50, 350, 150, 50, "ROCK", lambda: choose("ROCK")),
    Button(220, 350, 150, 50, "PAPER", lambda: choose("PAPER")),
    Button(390, 350, 150, 50, "SCISSORS", lambda: choose("SCISSORS")),
    Button(220, 420, 150, 50, "RESET", reset_game)
]

# 绘制选择图标
def draw_icon(surface, choice, x, y, size=60):
    if choice == "ROCK":
        pygame.draw.circle(surface, (180, 180, 200), (x, y), size//2, 3)
        pygame.draw.circle(surface, (150, 150, 180), (x, y), size//3, 2)
    elif choice == "PAPER":
        pygame.draw.rect(surface, (200, 230, 200), (x-size//2, y-size//2, size, size), 3, border_radius=10)
        pygame.draw.line(surface, (180, 210, 180), (x-size//2+5, y-size//2+5), (x+size//2-5, y+size//2-5), 2)
    elif choice == "SCISSORS":
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
        title = font_large.render("ROCK PAPER SCISSORS", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # 分数显示
        score_text = font_medium.render(f"Player: {score[0]}   Computer: {score[1]}   Ties: {score[2]}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 70))
        
        # 玩家和电脑选择区域
        pygame.draw.rect(screen, PANEL_COLOR, (50, 120, WIDTH-100, 180), border_radius=15)
        pygame.draw.line(screen, (100, 100, 120), (WIDTH//2, 120), (WIDTH//2, 300), 2)
        
        # 标签
        player_label = font_small.render("YOUR CHOICE", True, TEXT_COLOR)
        computer_label = font_small.render("COMPUTER CHOICE", True, TEXT_COLOR)
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
            color = RESULT_WIN if result == "YOU WIN!" else RESULT_LOSE if result == "COMPUTER WINS!" else RESULT_TIE
            result_text = font_large.render(result, True, color)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 300))
        
        # 绘制按钮
        for button in buttons:
            button.draw(screen)
        
        # 游戏规则提示
        rules = font_small.render("Rock beats Scissors | Paper beats Rock | Scissors beats Paper", True, (180, 180, 180))
        screen.blit(rules, (WIDTH//2 - rules.get_width()//2, 480))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()