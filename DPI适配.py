# 高DPI适配
# 解决在高DPI屏幕上GUI程序显示模糊的问题

try:
    # Windows 8.1及以上版本支持每进程DPI感知
    from ctypes import windll
    
    # 设置进程DPI感知级别为系统DPI感知 (每个监视器的DPI级别)
    # 1 表示系统级DPI感知，2表示每监视器DPI感知
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    # 如果shcore库不可用或调用失败，则使用较旧的API
    try:
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    except Exception:
        # 在非Windows系统或其他异常情况下忽略
        pass