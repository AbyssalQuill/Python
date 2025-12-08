from math import*
import re

def derivative(f, x, h=1e-8):
    """计算函数f在x点的导数近似值"""
    return (f(x + h) - f(x)) / h

# 安全的表达式解析函数
def safe_eval(expr, x):
    # 只允许特定的数学函数和操作
    allowed_names = {
        "sin": sin, "cos": cos, "tan": tan,
        "log": log, "exp": exp, "sqrt": sqrt,
        "abs": abs, "pow": pow, "x": x,
        "pi": pi, "e": e
    }
    
    # 检查表达式是否包含非法字符
    if re.search(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\(', expr):
        # 检查是否只包含允许的函数
        functions = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', expr)
        for func in functions:
            if func not in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt', 'abs', 'pow']:
                raise ValueError(f"不允许的函数: {func}")
    
    # 替换表达式中的x为数值
    expr = expr.replace('x', str(x))
    return eval(expr, {"__builtins__": {}}, allowed_names)

try:
    func_str = input("请输入函数表达式（使用x作为变量）：")
    
    # 将输入的字符串转换为可调用的函数
    def f(x):
        # 使用更安全的方式计算表达式
        return safe_eval(func_str, x)
    
    # 获取计算导数的点
    try:
        x_val = float(input("请输入计算导数的点x："))
    except ValueError:
        print("错误：请输入有效的数字")
        exit()
    
    # 计算导数并保留3位小数
    result = derivative(f, x_val)
    print(f"函数在x={x_val}处的导数近似值为：{round(result, 3)}")

except ValueError as e:
    print(f"输入错误：{e}")
except ZeroDivisionError:
    print("计算错误：除零错误")
except Exception as e:
    print(f"计算出错：{e}")