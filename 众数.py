# 寻找众数
def mode(num):
    if not num:  # 检查输入列表是否为空
        return '无众数'
    count_dict = {}
    # 统计每个数字出现的次数
    for n in num:
        if n in count_dict:
            count_dict[n] += 1
        else:
            count_dict[n] = 1
    # 找到最大的出现次数
    max_count = max(count_dict.values())
    # 收集所有出现次数等于最大次数的数字（可能有多个众数）
    modes = [k for k, v in count_dict.items() if v == max_count]
    # 如果所有数字出现次数都为1，则没有众数
    if max_count == 1:
        return '无众数'
    # 如果只有一个众数，直接返回该数字；否则返回众数列表
    return modes[0] if len(modes) == 1 else modes

# 修复输入处理部分：将输入按分隔符拆分并转换为数字
num_input = input('输入数组（用逗号分隔数字，例如1,2,3）：')
num = [int(x.strip()) for x in num_input.split(',')] if num_input else []
print(f'众数为{mode(num)}')

#方案二
# 寻找众数（使用count()方法）
def mode_count(num):
    if not num:  # 检查输入列表是否为空
        return '无众数'
    # 去重，避免重复统计相同元素
    unique_nums = list(set(num))
    # 用count()方法统计每个元素的出现次数
    count_list = [(n, num.count(n)) for n in unique_nums]
    # 找到最大的出现次数
    max_count = max(count for n, count in count_list)
    # 收集所有出现次数等于最大次数的数字（可能有多个众数）
    modes = [n for n, count in count_list if count == max_count]
    # 如果所有数字出现次数都为1，则没有众数
    if max_count == 1:
        return '无众数'
    # 如果只有一个众数，直接返回该数字；否则返回众数列表
    return modes[0] if len(modes) == 1 else modes

# 输入处理部分
num_input = input('输入数组（用逗号分隔数字，例如1,2,3）：')
num = [int(x.strip()) for x in num_input.split(',')] if num_input else []
print(f'众数为{mode_count(num)}')

        

