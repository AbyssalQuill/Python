import tkinter as tk
from tkinter import messagebox, ttk
import random
import sys
import ctypes
from enum import Enum

# -------------------------- 游戏常量定义 --------------------------
class ElementType(Enum):
    """元素类型枚举（使用红橙黄绿蓝紫六种易于区分的颜色）"""
    红色 = "#FF4444"    # 鲜明的红色
    橙色 = "#FF7700"    # 调整后的橙色，提高区分度
    黄色 = "#FFDD44"    # 柔和的黄色
    绿色 = "#00CC66"    # 清新的绿色
    蓝色 = "#3366FF"    # 鲜明的蓝色
    紫色 = "#AA33BB"    # 明显的紫色
    横向特效 = "#FF9800"
    纵向特效 = "#F44336"
    爆炸特效 = "#9C27B0"
    魔力鸟 = "#FFEB3B"

# 游戏配置
BASE_GRID_SIZE = 8
BASE_BLOCK_SIZE = 50
BASE_PADDING = 2
MAX_CHAIN_DEPTH = 20
MIN_TARGET_COUNT = 10     # 目标最小数量
MAX_TARGET_COUNT = 25     # 目标最大数量
STEP_CALCULATION_FACTOR = 0.7  # 步数计算因子，控制难度

# 界面颜色
BACKGROUND_COLOR = "#F8F9FA"
PANEL_COLOR = "#E9ECEF"
TEXT_COLOR = "#2D3436"
BUTTON_COLOR = "#FFFFFF"  # 白底
BUTTON_TEXT_COLOR = "#000000"  # 黑字
SELECTED_BORDER = "#3498DB"
NORMAL_BORDER = "#FFFFFF"

# 普通元素列表（红橙黄绿蓝紫）
REGULAR_ELEMENTS = [
    ElementType.红色,
    ElementType.橙色,
    ElementType.黄色,
    ElementType.绿色,
    ElementType.蓝色,
    ElementType.紫色
]

# -------------------------- 高DPI适配 --------------------------
class DPIHandler:
    """处理不同屏幕的DPI适配"""
    def __init__(self):
        self.scale_factor = self._get_scale_factor()
        
    def _get_scale_factor(self):
        """获取系统缩放因子"""
        try:
            if sys.platform.startswith('win'):
                ctypes.windll.user32.SetProcessDPIAware()
                return ctypes.windll.user32.GetDpiForSystem() / 96.0
            return 1.0
        except Exception:
            return 1.0
            
    def scale(self, value):
        """按系统缩放因子缩放值"""
        return int(value * self.scale_factor)

# -------------------------- 关卡目标类 --------------------------
class LevelObjective:
    """关卡目标类"""
    def __init__(self, target_type, required_count):
        self.target_type = target_type  # 目标元素类型
        self.required_count = required_count  # 需要收集的数量
        self.current_count = 0  # 当前收集数量
    
    def is_completed(self):
        """检查目标是否完成"""
        return self.current_count >= self.required_count
    
    def add_progress(self, count=1):
        """增加进度"""
        self.current_count = min(self.current_count + count, self.required_count)
    
    def get_progress_text(self):
        """获取进度文本（使用中文颜色名称）"""
        return f"{self.target_type.name}: {self.current_count}/{self.required_count}"

# -------------------------- 游戏核心类 --------------------------
class MatchThreeGame:
    def __init__(self, root):
        # DPI适配
        self.dpi = DPIHandler()
        
        # 主窗口设置
        self.root = root
        self.root.title("消消乐")
        self.root.geometry(f"{self.dpi.scale(900)}x{self.dpi.scale(700)}")
        self.root.minsize(700, 600)
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # 窗口居中
        self._center_window()
        
        # 游戏基础参数
        self.grid_size = BASE_GRID_SIZE
        self.block_size = self.dpi.scale(BASE_BLOCK_SIZE)
        self.padding = self.dpi.scale(BASE_PADDING)
        self.window_scale = 1.0
        
        # 游戏状态
        self.grid = []  # 游戏网格
        self.block_ids = []  # 画布元素ID
        self.selected_pos = (-1, -1)  # 选中位置
        self.score = 0
        self.remaining_steps = 0  # 剩余步数，动态计算
        self.max_steps = 0  # 最大步数
        self.is_processing = False  # 防止并行操作
        self.game_running = False
        self.chain_depth = 0  # 连锁深度
        self.combo_count = 0  # 连击计数
        
        # 关卡目标
        self.objectives = []
        self.objective_labels = []
        self.progress_frame = None
        
        # 创建界面
        self._create_widgets()
        
        # 窗口缩放处理
        self.resize_timer = None
        self.root.bind("<Configure>", self._on_resize)
        
        # 显示开始界面
        self.show_start_screen()

    def _center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        win_width = self.root.winfo_width()
        win_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")

    def _create_widgets(self):
        """创建所有界面组件"""
        self.main_container = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 开始界面和游戏界面
        self.start_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        self.game_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        self.game_frame.pack_forget()
        
        # 初始化子界面
        self._init_start_screen()
        self._init_game_screen()

    def _create_styled_button(self, parent, text, command, font_size=14, width=12):
        """创建统一样式的按钮（白底黑字）"""
        btn = tk.Button(
            parent,
            text=text,
            command=lambda: self._safe_execute(command),
            font=("微软雅黑", font_size),
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            relief=tk.RAISED,
            bd=1,
            width=width
        )
        return btn

    def _safe_execute(self, func):
        """安全执行函数，即使游戏结束也能响应"""
        try:
            # 对于返回和重新开始按钮，即使游戏正在处理中也允许执行
            if func in [self.show_start_screen, self.confirm_restart]:
                self.is_processing = False
                self.game_running = False
                func()
            elif not self.is_processing:
                func()
        except Exception as e:
            print(f"操作错误: {str(e)}")
            if self.game_running:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

    def _init_start_screen(self):
        """初始化开始界面"""
        center_frame = tk.Frame(self.start_frame, bg=BACKGROUND_COLOR)
        center_frame.pack(expand=True)
        
        # 标题
        tk.Label(
            center_frame,
            text="消消乐",
            font=("微软雅黑", 32, "bold"),
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        ).pack(pady=(0, 30))
        
        # 游戏规则
        rules = ["•本游戏由MrZ开发，游玩愉快",
            "• 交换相邻方块，3个及以上同色相连即可消除",
            "• 四连消除生成直线特效，五连生成魔力鸟",
            "• T/L形五连生成爆炸特效，特殊元素组合有惊喜",
            "• 根据方块分布智能计算步数，完成目标即可胜利"
        ]
        rule_frame = tk.Frame(center_frame, bg=BACKGROUND_COLOR)
        rule_frame.pack(pady=10)
        for rule in rules:
            tk.Label(
                rule_frame,
                text=rule,
                font=("微软雅黑", 12),
                fg=TEXT_COLOR,
                bg=BACKGROUND_COLOR
            ).pack(pady=5, anchor=tk.W)
        
        # 按钮
        btn_frame = tk.Frame(center_frame, bg=BACKGROUND_COLOR)
        btn_frame.pack(pady=30)
        
        self._create_styled_button(
            btn_frame,
            text="开始游戏",
            command=self.start_game,
            font_size=16,
            width=12
        ).pack(pady=8)
        
        self._create_styled_button(
            btn_frame,
            text="退出游戏",
            command=self.root.quit,
            font_size=16,
            width=12
        ).pack(pady=5)

    def _init_game_screen(self):
        """初始化游戏界面"""
        # 顶部状态栏
        status_frame = tk.Frame(self.game_frame, bg=PANEL_COLOR, padx=15, pady=8)
        status_frame.pack(fill=tk.X)
        
        # 左侧：分数
        left_frame = tk.Frame(status_frame, bg=PANEL_COLOR)
        left_frame.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(
            left_frame,
            text=f"分数: {self.score}",
            font=("微软雅黑", 14, "bold"),
            fg=TEXT_COLOR,
            bg=PANEL_COLOR
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.combo_label = tk.Label(
            left_frame,
            text="连击: 0",
            font=("微软雅黑", 12),
            fg="#E67E22",
            bg=PANEL_COLOR
        )
        self.combo_label.pack(side=tk.LEFT, padx=15)
        
        # 右侧：按钮 + 步数显示
        right_frame = tk.Frame(status_frame, bg=PANEL_COLOR)
        right_frame.pack(side=tk.RIGHT)
        
        # 步数显示标签
        self.step_label = tk.Label(
            right_frame,
            text=f"剩余步数: {self.remaining_steps}/{self.max_steps}",
            font=("微软雅黑", 14, "bold"),
            fg="#27AE60",
            bg=PANEL_COLOR
        )
        self.step_label.pack(side=tk.RIGHT, padx=15)
        
        self._create_styled_button(
            right_frame,
            text="重新开始",
            command=self.confirm_restart,
            font_size=12,
            width=10
        ).pack(side=tk.RIGHT, padx=10)
        
        self._create_styled_button(
            right_frame,
            text="返回开始",
            command=self.show_start_screen,
            font_size=12,
            width=10
        ).pack(side=tk.RIGHT, padx=10)
        
        # 中间区域：游戏区和目标区
        middle_frame = tk.Frame(self.game_frame, bg=BACKGROUND_COLOR)
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        # 游戏画布
        canvas_container = tk.Frame(middle_frame, bg=BACKGROUND_COLOR)
        canvas_container.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        
        self.game_canvas = tk.Canvas(
            canvas_container,
            bg=BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.game_canvas.pack(padx=10, pady=10)
        self.game_canvas.bind("<Button-1>", self._on_block_click)
        
        # 右侧目标面板
        self.objective_frame = tk.Frame(middle_frame, bg=PANEL_COLOR, padx=10, pady=10)
        self.objective_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(
            self.objective_frame,
            text="随机关卡目标",
            font=("微软雅黑", 14, "bold"),
            fg=TEXT_COLOR,
            bg=PANEL_COLOR
        ).pack(anchor=tk.W, pady=(0, 10))

    def confirm_restart(self):
        """确认重新开始游戏"""
        # 强制重置状态，确保按钮响应
        self.is_processing = False
        self.game_running = False
        
        if messagebox.askyesno("确认", "当前进度将丢失，确定重新开始？"):
            self.start_game()
        else:
            # 如果用户取消，恢复游戏状态
            self.game_running = True

    def _on_resize(self, event):
        """窗口缩放事件（防抖动）"""
        if not self.game_running or event.widget != self.root:
            return
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        self.resize_timer = self.root.after(100, lambda: self._do_resize(event))

    def _do_resize(self, event):
        """执行缩放逻辑"""
        base_width = self.dpi.scale(900)
        base_height = self.dpi.scale(700)
        width_ratio = event.width / base_width
        height_ratio = event.height / base_height
        self.window_scale = min(width_ratio, height_ratio)
        self.window_scale = max(self.window_scale, 0.6)
        
        self.block_size = int(self.dpi.scale(BASE_BLOCK_SIZE) * self.window_scale)
        self.padding = int(self.dpi.scale(BASE_PADDING) * self.window_scale)
        self._draw_blocks()
        self.resize_timer = None

    def show_start_screen(self):
        """切换到开始界面"""
        # 强制重置状态
        self.game_running = False
        self.is_processing = False
        self.game_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)

    def start_game(self):
        """开始游戏"""
        if self.is_processing:
            return
        self.is_processing = True
        
        try:
            # 切换界面
            self.start_frame.pack_forget()
            self.game_frame.pack(fill=tk.BOTH, expand=True)
            
            # 重置游戏状态
            self.score = 0
            self.selected_pos = (-1, -1)
            self.chain_depth = 0
            self.combo_count = 0
            self.game_running = True
            
            # 清空画布
            self.game_canvas.delete("all")
            self.block_ids = []
            
            # 初始化随机目标
            self._init_level_objectives()
            
            # 生成初始网格
            self._generate_valid_grid()
            
            # 计算并设置步数（在网格生成后进行）
            self._calculate_steps_based_on_grid()
            
            # 更新界面显示
            self.score_label.config(text=f"分数: {self.score}")
            self.combo_label.config(text="连击: 0")
            self.step_label.config(text=f"剩余步数: {self.remaining_steps}/{self.max_steps}")
        finally:
            self.is_processing = False

    def _count_element_in_grid(self, element_type):
        """统计网格中特定元素的数量"""
        count = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] == element_type:
                    count += 1
        return count

    def _calculate_steps_based_on_grid(self):
        """根据网格分布和目标计算所需步数"""
        total_required = sum(obj.required_count for obj in self.objectives)
        total_available = sum(self._count_element_in_grid(obj.target_type) for obj in self.objectives)
        
        # 计算基础步数：目标总数 ÷ 平均每步可消除的数量(约3-4个)
        base_steps = total_required / 3.5
        
        # 根据元素分布调整：元素越分散，需要的步数越多
        distribution_factor = 1.0
        for obj in self.objectives:
            # 检查元素是否分散
            elements = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) 
                       if self.grid[r][c] == obj.target_type]
            
            if len(elements) > 0:
                # 计算元素的分散程度（基于坐标标准差）
                avg_r = sum(r for r, c in elements) / len(elements)
                avg_c = sum(c for r, c in elements) / len(elements)
                
                std_dev = sum(((r-avg_r)**2 + (c-avg_c)** 2) for r, c in elements) / len(elements)
                distribution_factor += std_dev / 50  # 标准化分散因子
        
        # 综合计算步数
        calculated_steps = base_steps * distribution_factor * (1 / STEP_CALCULATION_FACTOR)
        
        # 确保步数在合理范围内
        min_possible_steps = max(10, int(total_required / 5))  # 最少步数
        max_possible_steps = min(80, int(total_required / 2))  # 最多步数
        self.max_steps = int(max(min_possible_steps, min(max_possible_steps, calculated_steps)))
        self.remaining_steps = self.max_steps

    def _init_level_objectives(self):
        """初始化关卡目标"""
        # 清除现有目标
        for widget in self.objective_labels:
            widget.destroy()
        self.objective_labels = []
        
        # 销毁旧进度条
        if self.progress_frame and self.progress_frame.winfo_exists():
            self.progress_frame.destroy()
        
        # 创建新目标（随机类型和数量）
        target_types = random.sample(REGULAR_ELEMENTS, 3)
        self.objectives = [
            LevelObjective(target_types[0], random.randint(MIN_TARGET_COUNT, MAX_TARGET_COUNT)),
            LevelObjective(target_types[1], random.randint(MIN_TARGET_COUNT, MAX_TARGET_COUNT)),
            LevelObjective(target_types[2], random.randint(MIN_TARGET_COUNT, MAX_TARGET_COUNT))
        ]
        
        # 显示目标（使用中文颜色名称）
        for obj in self.objectives:
            label = tk.Label(
                self.objective_frame,
                text=obj.get_progress_text(),
                font=("微软雅黑", 12),
                fg=TEXT_COLOR,
                bg=PANEL_COLOR
            )
            label.pack(anchor=tk.W, pady=5)
            self.objective_labels.append(label)
        
        # 添加进度条
        self.progress_frame = tk.Frame(self.objective_frame, bg=PANEL_COLOR)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.level_progress = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            length=100,
            mode="determinate"
        )
        self.level_progress.pack(fill=tk.X)
        self._update_level_progress()

    def _update_level_progress(self):
        """更新关卡进度"""
        completed = sum(1 for obj in self.objectives if obj.is_completed())
        progress = int((completed / len(self.objectives)) * 100)
        self.level_progress["value"] = progress
        return completed == len(self.objectives)

    def _generate_valid_grid(self):
        """生成有效的初始网格"""
        if not self.game_running:
            return
        
        max_attempts = 150
        attempts = 0
        
        while attempts < max_attempts:
            # 生成随机网格（只包含普通元素）
            self.grid = [[random.choice(REGULAR_ELEMENTS) for _ in range(BASE_GRID_SIZE)] 
                         for _ in range(BASE_GRID_SIZE)]
            # 检查是否有可消除的组合
            if not self._find_removable_blocks():
                self._draw_blocks()
                return
            attempts += 1
        
        # 多次尝试失败，强制使用当前网格
        self._draw_blocks()
        messagebox.showinfo("提示", "已进入游戏，部分方块可直接消除")

    def _draw_blocks(self):
        """绘制游戏方块"""
        if not self.game_running:
            return
        
        # 设置画布大小
        canvas_size = self.grid_size * (self.block_size + self.padding)
        self.game_canvas.config(width=canvas_size, height=canvas_size)
        
        # 首次绘制
        if not self.block_ids:
            for row in range(self.grid_size):
                row_ids = []
                for col in range(self.grid_size):
                    x1 = col * (self.block_size + self.padding)
                    y1 = row * (self.block_size + self.padding)
                    x2 = x1 + self.block_size
                    y2 = y1 + self.block_size
                    
                    # 获取颜色
                    element = self.grid[row][col]
                    color = element.value if element is not None else BACKGROUND_COLOR
                    
                    # 绘制方块
                    block_id = self.game_canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline=NORMAL_BORDER,
                        width=2
                    )
                    
                    # 为特殊元素添加标记
                    if element == ElementType.横向特效:
                        self.game_canvas.create_line(
                            x1 + 5, y1 + self.block_size//2,
                            x2 - 5, y1 + self.block_size//2,
                            width=3, fill="white"
                        )
                    elif element == ElementType.纵向特效:
                        self.game_canvas.create_line(
                            x1 + self.block_size//2, y1 + 5,
                            x1 + self.block_size//2, y2 - 5,
                            width=3, fill="white"
                        )
                    elif element == ElementType.爆炸特效:
                        self.game_canvas.create_oval(
                            x1 + 10, y1 + 10,
                            x2 - 10, y2 - 10,
                            outline="white", width=3
                        )
                    elif element == ElementType.魔力鸟:
                        self.game_canvas.create_text(
                            x1 + self.block_size//2, y1 + self.block_size//2,
                            text="魔", font=("微软雅黑", 12, "bold"), fill="black"
                        )
                    
                    row_ids.append(block_id)
                self.block_ids.append(row_ids)
        # 更新现有方块
        else:
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    element = self.grid[row][col]
                    color = element.value if element is not None else BACKGROUND_COLOR
                    self.game_canvas.itemconfig(self.block_ids[row][col], fill=color)
                    self.game_canvas.itemconfig(
                        self.block_ids[row][col],
                        outline=NORMAL_BORDER,
                        width=2
                    )

    def _get_clicked_block(self, x, y):
        """获取点击的方块位置"""
        if not self.game_running or self.is_processing:
            return (-1, -1)
        
        col = x // (self.block_size + self.padding)
        row = y // (self.block_size + self.padding)
        
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return (row, col)
        return (-1, -1)

    def _on_block_click(self, event):
        """处理方块点击事件"""
        if self.is_processing or not self.game_running:
            return
        
        click_row, click_col = self._get_clicked_block(event.x, event.y)
        
        if (click_row, click_col) == (-1, -1):
            self._reset_selected()
            return
        
        if (click_row, click_col) == self.selected_pos:
            self._reset_selected()
            return
        
        if self.selected_pos == (-1, -1):
            self.selected_pos = (click_row, click_col)
            self._highlight_block(click_row, click_col)
            return
        
        # 处理交换
        prev_row, prev_col = self.selected_pos
        if self._is_adjacent(prev_row, prev_col, click_row, click_col):
            self._swap_blocks(prev_row, prev_col, click_row, click_col)
        else:
            self._reset_selected()
            self.selected_pos = (click_row, click_col)
            self._highlight_block(click_row, click_col)

    def _is_adjacent(self, r1, c1, r2, c2):
        """判断两个方块是否相邻"""
        return max(abs(r1 - r2), abs(c1 - c2)) == 1

    def _highlight_block(self, row, col):
        """高亮选中的方块"""
        self.game_canvas.itemconfig(
            self.block_ids[row][col],
            outline=SELECTED_BORDER,
            width=3
        )

    def _reset_selected(self):
        """重置选中状态"""
        if self.selected_pos != (-1, -1):
            row, col = self.selected_pos
            self.game_canvas.itemconfig(
                self.block_ids[row][col],
                outline=NORMAL_BORDER,
                width=2
            )
        self.selected_pos = (-1, -1)

    def _swap_blocks(self, r1, c1, r2, c2):
        """交换两个方块"""
        self.is_processing = True
        self._reset_selected()
        
        # 保存原始元素用于恢复
        original1 = self.grid[r1][c1]
        original2 = self.grid[r2][c2]
        
        # 检查是否是魔力鸟交换
        if original1 == ElementType.魔力鸟 or original2 == ElementType.魔力鸟:
            self._handle_bird_swap(r1, c1, r2, c2, original1, original2)
            return
        
        # 普通交换
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
        self._update_block_color(r1, c1)
        self._update_block_color(r2, c2)
        
        # 延迟检查消除
        self.root.after(200, lambda: self._check_eliminate(original1, original2, r1, c1, r2, c2))

    def _handle_bird_swap(self, r1, c1, r2, c2, original1, original2):
        """处理魔力鸟交换"""
        # 魔力鸟与普通元素交换：消除所有同色元素
        if original1 == ElementType.魔力鸟 and original2 in REGULAR_ELEMENTS:
            color_to_clear = original2
            removable = [(row, col) for row in range(self.grid_size) 
                         for col in range(self.grid_size) 
                         if self.grid[row][col] == color_to_clear]
            self._process_elimination(removable)
            return
            
        if original2 == ElementType.魔力鸟 and original1 in REGULAR_ELEMENTS:
            color_to_clear = original1
            removable = [(row, col) for row in range(self.grid_size) 
                         for col in range(self.grid_size) 
                         if self.grid[row][col] == color_to_clear]
            self._process_elimination(removable)
            return
            
        # 魔力鸟与魔力鸟交换：清空整个棋盘
        if original1 == ElementType.魔力鸟 and original2 == ElementType.魔力鸟:
            removable = [(row, col) for row in range(self.grid_size) 
                         for col in range(self.grid_size)]
            self._process_elimination(removable)
            return
            
        # 魔力鸟与其他特殊元素交换
        if original1 == ElementType.魔力鸟 and original2 in [ElementType.横向特效, ElementType.纵向特效, ElementType.爆炸特效]:
            self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
            self._trigger_special_element(r2, c2)
            return
            
        if original2 == ElementType.魔力鸟 and original1 in [ElementType.横向特效, ElementType.纵向特效, ElementType.爆炸特效]:
            self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
            self._trigger_special_element(r1, c1)
            return

    def _update_block_color(self, row, col):
        """更新单个方块的颜色"""
        element = self.grid[row][col]
        color = element.value if element is not None else BACKGROUND_COLOR
        self.game_canvas.itemconfig(self.block_ids[row][col], fill=color)

    def _find_removable_blocks(self):
        """查找所有可消除的方块 - 改进相同方块检测逻辑"""
        removable = set()
        visited = set()
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                current_element = self.grid[row][col]
                # 只处理普通元素
                if (row, col) not in visited and current_element is not None and current_element in REGULAR_ELEMENTS:
                    # 检查水平和垂直方向是否有可消除组合
                    if self._check_line(row, col, 0, 1) or self._check_line(row, col, 1, 0):
                        # 找到所有连通的同色元素
                        connected = self._get_connected_blocks(row, col, visited)
                        for (r, c) in connected:
                            removable.add((r, c))
        
        return list(removable)

    def _check_line(self, row, col, dr, dc):
        """检查直线上是否有三连或以上 - 修复边界检测问题"""
        element = self.grid[row][col]
        if element is None or element not in REGULAR_ELEMENTS:
            return False
            
        count = 1
        
        # 向一个方向检查
        r, c = row + dr, col + dc
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size:
            if self.grid[r][c] == element:
                count += 1
                r += dr
                c += dc
            else:
                break
            
        # 向相反方向检查
        r, c = row - dr, col - dc
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size:
            if self.grid[r][c] == element:
                count += 1
                r -= dr
                c -= dc
            else:
                break
        
        return count >= 3

    def _get_connected_blocks(self, start_row, start_col, visited):
        """获取所有连通的同色方块 - 改进连通性检测"""
        target = self.grid[start_row][start_col]
        if target is None or target not in REGULAR_ELEMENTS:
            return []
        
        # 检查上下左右四个方向
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        queue = [(start_row, start_col)]
        visited.add((start_row, start_col))
        connected = [(start_row, start_col)]
        
        while queue:
            row, col = queue.pop(0)
            for dr, dc in directions:
                new_row = row + dr
                new_col = col + dc
                # 严格检查是否为相同元素
                if (0 <= new_row < self.grid_size and
                    0 <= new_col < self.grid_size and
                    (new_row, new_col) not in visited and
                    self.grid[new_row][new_col] == target):
                    visited.add((new_row, new_col))
                    connected.append((new_row, new_col))
                    queue.append((new_row, new_col))
        
        return connected

    def _check_eliminate(self, orig1, orig2, r1, c1, r2, c2):
        """检查交换后是否可消除 - 增加二次确认步骤"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 查找可消除的方块
        removable = self._find_removable_blocks()
        
        # 检查是否有特殊元素需要触发
        special_removables = []
        if removable:
            for (row, col) in removable:
                element = self.grid[row][col]
                if element in [ElementType.横向特效, ElementType.纵向特效, ElementType.爆炸特效]:
                    special_removables.append((row, col))
        
        # 处理特殊元素
        if special_removables:
            # 先清除基础消除的方块
            for (row, col) in removable:
                if (row, col) not in special_removables:
                    self.grid[row][col] = None
            
            self._draw_blocks()
            self.root.after(200, lambda: self._process_special_elements(special_removables))
            return
        
        # 如果没有可消除的方块，恢复原状（不消耗步数）
        if not removable:
            self.grid[r1][c1] = orig1
            self.grid[r2][c2] = orig2
            self._update_block_color(r1, c1)
            self._update_block_color(r2, c2)
            self.is_processing = False
            return
        
        # 有有效消除：消耗1步
        self.remaining_steps -= 1
        self.step_label.config(text=f"剩余步数: {self.remaining_steps}/{self.max_steps}")
        
        # 步数耗尽：直接结束游戏
        if self.remaining_steps <= 0:
            self.root.after(500, lambda: self.game_over(False))
            self.is_processing = False
            return
        
        # 处理普通消除
        self._process_elimination(removable)

    def _process_special_elements(self, special_elements):
        """处理特殊元素的触发"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 收集所有要消除的方块
        all_removable = set()
        
        for (row, col) in special_elements:
            element = self.grid[row][col]
            if element == ElementType.横向特效:
                # 横向特效：消除整行
                for c in range(self.grid_size):
                    all_removable.add((row, c))
            elif element == ElementType.纵向特效:
                # 纵向特效：消除整列
                for r in range(self.grid_size):
                    all_removable.add((r, col))
            elif element == ElementType.爆炸特效:
                # 爆炸特效：消除3x3范围
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r = row + dr
                        c = col + dc
                        if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                            all_removable.add((r, c))
        
        # 执行消除
        self._process_elimination(list(all_removable))

    def _trigger_special_element(self, row, col):
        """触发单个特殊元素"""
        if not self.game_running:
            self.is_processing = False
            return
        
        element = self.grid[row][col]
        if element is None:
            self.is_processing = False
            return
            
        removable = []
        
        if element == ElementType.横向特效:
            # 横向特效：消除整行
            for c in range(self.grid_size):
                removable.append((row, c))
        elif element == ElementType.纵向特效:
            # 纵向特效：消除整列
            for r in range(self.grid_size):
                removable.append((r, col))
        elif element == ElementType.爆炸特效:
            # 爆炸特效：消除3x3范围
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                        removable.append((r, c))
        
        # 执行消除
        self._process_elimination(removable)

    def _process_elimination(self, removable):
        """处理消除逻辑"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 记录被消除的元素类型
        eliminated_elements = []
        for (row, col) in removable:
            element = self.grid[row][col]
            if element is not None and element in REGULAR_ELEMENTS:
                eliminated_elements.append(element)
        
        # 计算得分
        base_points = len(removable) * 10
        combo_multiplier = 1 + (self.combo_count // 3) * 0.2  # 每3连击增加20%得分
        total_points = int(base_points * combo_multiplier)
        self.score += total_points
        self.score_label.config(text=f"分数: {self.score}")
        
        # 更新连击计数
        self.combo_count += 1
        self.combo_label.config(text=f"连击: {self.combo_count}")
        
        # 标记消除的方块
        for (row, col) in removable:
            self.grid[row][col] = None
        
        # 更新目标进度
        for elem in eliminated_elements:
            for obj in self.objectives:
                if obj.target_type == elem and not obj.is_completed():
                    obj.add_progress()
        
        # 更新目标显示
        for i, obj in enumerate(self.objectives):
            self.objective_labels[i].config(text=obj.get_progress_text())
        
        # 检查关卡是否完成
        if self._update_level_progress():
            self.root.after(500, lambda: self.game_over(True))
            return
        
        # 更新显示
        self._draw_blocks()
        
        # 延迟执行方块下落
        self.root.after(300, self._drop_blocks)

    def _generate_special_element(self, pattern, positions):
        """根据消除模式生成特殊元素"""
        if not positions:
            return None
            
        # 计算中心位置
        center_idx = len(positions) // 2
        center_row, center_col = positions[center_idx]
        
        # 根据模式生成特殊元素
        if pattern == "horizontal_4":  # 横向四连
            return (center_row, center_col, ElementType.横向特效)
        elif pattern == "vertical_4":  # 纵向四连
            return (center_row, center_col, ElementType.纵向特效)
        elif pattern == "horizontal_5" or pattern == "vertical_5":  # 五连
            return (center_row, center_col, ElementType.魔力鸟)
        elif pattern == "l_shape" or pattern == "t_shape":  # L形或T形五连
            return (center_row, center_col, ElementType.爆炸特效)
        
        return None

    def _detect_elimination_pattern(self, removable):
        """检测消除模式，用于生成特殊元素"""
        if len(removable) < 4:
            return None, []
            
        # 按行和列分组
        rows = {}
        cols = {}
        for (r, c) in removable:
            if r not in rows:
                rows[r] = []
            rows[r].append(c)
            if c not in cols:
                cols[c] = []
            cols[c].append(r)
        
        # 检查是否有四连或五连
        for r, cs in rows.items():
            cs_sorted = sorted(cs)
            # 检查连续的列
            for i in range(len(cs_sorted) - 3):
                if cs_sorted[i+3] - cs_sorted[i] == 3:  # 四连
                    return "horizontal_4", [(r, cs_sorted[i]), (r, cs_sorted[i+1]), 
                                          (r, cs_sorted[i+2]), (r, cs_sorted[i+3])]
            if len(cs_sorted) >= 5:
                for i in range(len(cs_sorted) - 4):
                    if cs_sorted[i+4] - cs_sorted[i] == 4:  # 五连
                        return "horizontal_5", [(r, cs_sorted[i]), (r, cs_sorted[i+1]), 
                                              (r, cs_sorted[i+2]), (r, cs_sorted[i+3]), (r, cs_sorted[i+4])]
        
        for c, rs in cols.items():
            rs_sorted = sorted(rs)
            # 检查连续的行
            for i in range(len(rs_sorted) - 3):
                if rs_sorted[i+3] - rs_sorted[i] == 3:  # 四连
                    return "vertical_4", [(rs_sorted[i], c), (rs_sorted[i+1], c), 
                                        (rs_sorted[i+2], c), (rs_sorted[i+3], c)]
            if len(rs_sorted) >= 5:
                for i in range(len(rs_sorted) - 4):
                    if rs_sorted[i+4] - rs_sorted[i] == 4:  # 五连
                        return "vertical_5", [(rs_sorted[i], c), (rs_sorted[i+1], c), 
                                            (rs_sorted[i+2], c), (rs_sorted[i+3], c), (rs_sorted[i+4], c)]
        
        # 检查L形或T形（五连）
        if len(removable) == 5:
            positions_set = set(removable)
            for (r, c) in removable:
                neighbors = 0
                # 检查四个方向
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (r+dr, c+dc) in positions_set:
                        neighbors += 1
                if neighbors >= 3:  # 中心位置至少连接3个方向
                    if any((r+dr, c+dc) in positions_set for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]):
                        return "l_shape", removable
                    else:
                        return "t_shape", removable
        
        return None, []

    def _drop_blocks(self):
        """重力下落：让元素下落填补空位 - 修复下落逻辑"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 按列处理，确保每个方块都能正确下落
        for col in range(self.grid_size):
            # 从底部向上处理，确保下落正确
            empty_spots = 0
            for row in range(self.grid_size-1, -1, -1):
                if self.grid[row][col] is None:
                    empty_spots += 1
                elif empty_spots > 0:
                    # 将方块下移到空位
                    self.grid[row + empty_spots][col] = self.grid[row][col]
                    self.grid[row][col] = None
        
        # 更新显示
        self._draw_blocks()
        
        # 延迟填充新元素
        self.root.after(300, self._fill_new_blocks)

    def _fill_new_blocks(self):
        """顶部填充：生成新元素填补顶部空位 - 修复新方块生成逻辑"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 填充新元素到顶部空位
        new_elements_added = False
        for col in range(self.grid_size):
            for row in range(self.grid_size):
                if self.grid[row][col] is None:
                    # 生成新元素时避免立即形成三连
                    new_element = self._get_valid_new_element(row, col)
                    self.grid[row][col] = new_element
                    new_elements_added = True
        
        # 更新显示
        self._draw_blocks()
        
        # 检查连锁反应
        if new_elements_added:
            self.chain_depth += 1
            if self.chain_depth < MAX_CHAIN_DEPTH:
                self.root.after(300, self._check_chain_reaction)
            else:
                # 超过最大连锁深度，结束连锁
                self.chain_depth = 0
                self.is_processing = False
        else:
            self.chain_depth = 0
            self.is_processing = False

    def _get_valid_new_element(self, row, col):
        """获取有效的新元素，避免在生成时就形成三连"""
        # 检查当前位置可能的冲突
        left1 = self.grid[row][col-1] if col > 0 else None
        left2 = self.grid[row][col-2] if col > 1 else None
        up1 = self.grid[row-1][col] if row > 0 else None
        up2 = self.grid[row-2][col] if row > 1 else None
        
        # 可能的候选元素
        candidates = REGULAR_ELEMENTS.copy()
        
        # 如果左边已有两个相同元素，排除该元素
        if left1 is not None and left2 == left1:
            if left1 in candidates:
                candidates.remove(left1)
        
        # 如果上边已有两个相同元素，排除该元素
        if up1 is not None and up2 == up1:
            if up1 in candidates and up1 in candidates:
                candidates.remove(up1)
        
        # 如果没有合适的候选元素（很少见），返回任意元素
        return random.choice(candidates) if candidates else random.choice(REGULAR_ELEMENTS)

    def _check_chain_reaction(self):
        """检查连锁反应：新布局是否有可消除的组合 - 增强连锁检测"""
        if not self.game_running:
            self.is_processing = False
            return
        
        # 查找可消除的方块
        removable = self._find_removable_blocks()
        
        # 检查是否有特殊元素需要处理
        special_removables = []
        if removable:
            for (row, col) in removable:
                element = self.grid[row][col]
                if element in [ElementType.横向特效, ElementType.纵向特效, ElementType.爆炸特效]:
                    special_removables.append((row, col))
        
        if special_removables:
            # 处理特殊元素
            for (row, col) in removable:
                if (row, col) not in special_removables:
                    self.grid[row][col] = None
            
            self._draw_blocks()
            self.root.after(200, lambda: self._process_special_elements(special_removables))
            return
        
        if removable:
            # 检测消除模式，生成特殊元素
            pattern, positions = self._detect_elimination_pattern(removable)
            special_element = self._generate_special_element(pattern, positions)
            
            # 执行消除
            self._process_elimination(removable)
            
            # 如果需要生成特殊元素
            if special_element:
                r, c, elem_type = special_element
                self.root.after(500, lambda: self._replace_with_special(r, c, elem_type))
                
            return
        else:
            # 没有连锁反应，重置状态
            self.chain_depth = 0
            self.is_processing = False

    def _replace_with_special(self, row, col, elem_type):
        """替换普通元素为特殊元素"""
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.grid[row][col] = elem_type
            self._update_block_color(row, col)

    def game_over(self, is_win):
        """游戏结束处理"""
        # 确保游戏状态被正确重置
        self.game_running = False
        self.is_processing = False  # 允许按钮响应
        
        # 显示结果
        if is_win:
            message = f"恭喜胜利！\n目标全部完成\n本次得分: {self.score}\n剩余步数: {self.remaining_steps}/{self.max_steps}"
        else:
            message = f"步数耗尽！\n本次得分: {self.score}\n目标完成度: {self.level_progress['value']}%"
        
        # 使用after确保UI更新完成后再显示消息框
        self.root.after(100, lambda: self._show_game_over_message(message, is_win))

    def _show_game_over_message(self, message, is_win):
        """显示游戏结束消息并处理后续操作"""
        result = messagebox.askyesno("游戏结束", f"{message}\n\n是否重新开始？")
        if result:
            self.start_game()
        else:
            self.show_start_screen()

# -------------------------- 程序入口 --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.option_add("*Font", "微软雅黑 10")
    except Exception:
        pass
    app = MatchThreeGame(root)
    root.mainloop()
