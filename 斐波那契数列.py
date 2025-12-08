#斐波那契额数列运行时间统计
from encodings.punycode import T
import time
start = time.time()
print("开始运行...")
def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

print(fib(1))
end = time.time()
print(f"运行结束，运行时间：{end - start}秒")


