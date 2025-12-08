import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import threading
import ctypes
import tempfile
class PyToExeConverter:
    def __init__(self, root):
        if sys.platform.startswith('win'):
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass
        
        self.root = root
        self.root.title("Python 转 EXE 工具")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)
        
        #存储转换后的ICO路径
        self.converted_icon_path = None
        
        #设置高清字体
        default_font = ('Microsoft YaHei UI', 10)   #微软雅黑UI
        title_font = ('Microsoft YaHei UI', 16, 'bold')
        
        #配置样式
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=default_font)
        self.style.configure('TButton', font=default_font, padding=5)  #按钮
        self.style.configure('Title.TLabel', font=title_font)
        self.style.configure('TCheckbutton', font=default_font)  #复选框
        self.style.configure('TEntry', font=default_font)  #输入框
        
        #进度条样式优化
        self.style.configure('TProgressbar', thickness=8)
        
        self.create_widgets()
    
    def create_widgets(self):
        #主框架
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #标题
        title_label = ttk.Label(main_frame, text="Python 转 EXE 工具", style='Title.TLabel')
        title_label.pack(pady=(0, 25))
        
        #选择文件区域
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=12)
        
        ttk.Label(file_frame, text="选择Python脚本:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.file_path = tk.StringVar()
        #输入框增加高度，更清晰
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=55)
        file_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.EW)
        
        browse_btn = ttk.Button(file_frame, text="浏览", command=self.browse_file)
        browse_btn.grid(row=1, column=1)
        
        file_frame.columnconfigure(0, weight=1)
        
        #选项区域
        options_frame = ttk.LabelFrame(main_frame, text="打包选项", padding="15 10 15 10")
        options_frame.pack(fill=tk.X, pady=12)
        
        #优化选项区域网格布局
        options_frame.grid_columnconfigure(1, pad=15)
        
        ttk.Label(options_frame, text="EXE名称:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.exe_name = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.exe_name, width=35).grid(row=0, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(options_frame, text="图标(可选):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.icon_path = tk.StringVar()
        icon_entry = ttk.Entry(options_frame, textvariable=self.icon_path, width=35)
        icon_entry.grid(row=1, column=1, sticky=tk.W, pady=8)
        
        icon_browse_btn = ttk.Button(options_frame, text="选择图标", command=self.browse_icon)
        icon_browse_btn.grid(row=1, column=2, padx=(5, 0))
        
        self.onefile = tk.BooleanVar(value=True)
        #复选框
        ttk.Checkbutton(options_frame, text="打包成单个EXE文件", variable=self.onefile).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=8, padx=(0, 0))
        
        self.console = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="显示控制台窗口", variable=self.console).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=8)
        
        #按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        #按钮
        self.convert_btn = ttk.Button(button_frame, text="开始转换", command=self.start_conversion, width=12)
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        exit_btn = ttk.Button(button_frame, text="退出", command=self.root.quit, width=8)
        exit_btn.pack(side=tk.LEFT)
        
        #进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=12)
        
        #日志区域
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="10 10 10 10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=12)
        
        #日志文本框
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame, 
            height=12, 
            width=75, 
            yscrollcommand=log_scrollbar.set,
            font=('Consolas', 10),  #等宽字体
            wrap=tk.WORD,  #自动换行
            relief=tk.FLAT  #扁平化边框
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        log_scrollbar.config(command=self.log_text.yview)
        
        #绑定事件
        file_entry.bind('<KeyRelease>', self.update_exe_name)
        
        #检查所需依赖是否已安装
        self.check_dependencies()
    

    def check_dependencies(self):
        #检查PyInstaller
        try:
            import PyInstaller
            self.log("PyInstaller 已安装")
        except ImportError:
            self.log("PyInstaller 未安装，正在安装...")
            self.install_dependency("pyinstaller")
        
        #检查Pillow
        try:
            from PIL import Image
            self.log("Pillow 已安装（用于图片转换）")
        except ImportError:
            self.log("Pillow 未安装，正在安装（用于图片转换）...")
            self.install_dependency("Pillow")
    
    def install_dependency(self, package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            self.log(f"{package} 安装成功!")
        except Exception as e:
            self.log(f"{package} 安装失败: {str(e)}")
            messagebox.showerror("错误", f"{package} 安装失败: {str(e)}")
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择Python脚本",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.update_exe_name()
    
    def browse_icon(self):
        """选择图标文件，并自动转换非ICO格式为ICO"""
        #支持更多图片格式
        filename = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[
                ("图片文件", "*.ico *.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        
        if filename:
            #检查文件扩展名
            ext = os.path.splitext(filename)[1].lower()
            
            #如果不是ICO格式，进行转换
            if ext != '.ico':
                self.log(f"检测到非ICO格式图片 ({ext})，正在转换为ICO格式...")    
                #调用转换函数
                ico_path = self.convert_to_ico(filename)
                
                if ico_path:
                    self.icon_path.set(filename)  #显示原始文件路径
                    self.converted_icon_path = ico_path  #保存转换后的路径
                    self.log(f"图片已成功转换为ICO格式: {os.path.basename(ico_path)}")
                else:
                    self.log("图片转换失败，未设置图标")
                    self.icon_path.set("")
                    self.converted_icon_path = None
            else:
                self.icon_path.set(filename)
                self.converted_icon_path = filename
                self.log("已选择ICO格式图标")
    
    def convert_to_ico(self, image_path):
        try:
            from PIL import Image
            
            #创建临时文件保存转换后的ICO
            temp_dir = tempfile.gettempdir()
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            ico_path = os.path.join(temp_dir, f"{base_name}_converted.ico")
            
            with Image.open(image_path) as img:
                sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
                
                #保存为ICO
                img.save(ico_path, format='ICO', sizes=sizes)
            
            return ico_path
            
        except Exception as e:
            self.log(f"图片转换错误: {str(e)}")
            messagebox.showerror("转换错误", f"无法将图片转换为ICO格式: {str(e)}")
            return None
    
    def update_exe_name(self, event=None):
        if not self.exe_name.get() and self.file_path.get():
            base_name = os.path.splitext(os.path.basename(self.file_path.get()))[0]
            self.exe_name.set(base_name)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        self.convert_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.convert)
        thread.daemon = True
        thread.start()
    
    def convert(self):
        if not self.file_path.get():
            messagebox.showerror("错误", "请先选择要转换的Python文件")
            self.convert_btn.config(state=tk.NORMAL)
            return
        
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("错误", "选择的Python文件不存在")
            self.convert_btn.config(state=tk.NORMAL)
            return
        
        cmd = [sys.executable, '-m', 'PyInstaller', '--noconfirm']
        
        if self.onefile.get():
            cmd.append('--onefile')
        
        if not self.console.get():
            cmd.append('--windowed')
        
        #使用转换后的ICO路径
        icon_to_use = self.converted_icon_path if self.converted_icon_path else self.icon_path.get()
        if icon_to_use and os.path.exists(icon_to_use):
            cmd.extend(['--icon', os.path.abspath(icon_to_use)])
        
        if self.exe_name.get():
            cmd.extend(['--name', self.exe_name.get()])
        cmd.append(os.path.abspath(self.file_path.get()))

        self.log("开始打包过程...")
        self.log("执行命令: "+' '.join(cmd)) 
        self.progress.start()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=os.path.dirname(os.path.abspath(self.file_path.get()))
            ) 
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log("打包成功完成!")
                messagebox.showinfo("成功", "EXE文件已生成在dist目录中")
            else:
                self.log("打包失败!")
                messagebox.showerror("错误", "打包过程失败，请查看日志获取详细信息")
                
        except Exception as e:
            self.log(f"发生错误: {str(e)}")
            messagebox.showerror("错误", f"打包过程发生异常: {str(e)}")
        finally:
            self.progress.stop()
            self.convert_btn.config(state=tk.NORMAL)
def main():
    root=tk.Tk()
    app=PyToExeConverter(root)
    root.mainloop()

if __name__=="__main__":
    main()
    