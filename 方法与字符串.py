name = "Ada Lovelace"
print(name.upper())#全大写，即把字符串中的所有字母转换为大写
print(name.lower())#全小写，即把字符串中的所有字母转换为小写
print(name.title())#每个单词首字母大写，即把字符串中的每个单词的首字母转换为大写，其余字母转换为小写
print(name.capitalize())#首字母大写
print(name.swapcase())#大写变小写，小写变大写
print(name.center(50, '*'))#居中对齐，填充字符为'*'
print(name.ljust(50, '*'))#左对齐，填充字符为'*'
print(name.rjust(50, '*'))#右对齐，填充字符为'*
print(name.strip())#去除首尾空格
print(name.lstrip())#去除左侧空格
print(name.rstrip())#去除右侧空格
print(name.replace("Ada", "Ada Byron"))#替换字符串
print(name.find("Lovelace"))#查找子字符串位置，若不存在则返回-1，
print(name.index("Lovelace"))#查找子字符串位置，若不存在则抛出异常
print(name.count("a"))#统计子字符串出现次数
print(name.startswith("Ada"))#检查字符串是否以指定子字符串开头
print(name.endswith("Lovelace"))#检查字符串是否以指定子字符串结尾
print(name.split())#分割字符串，默认按空格分割
print(name.split(','))#按逗号分割
print(name.split(' '))#按空格分割
print(name.splitlines())#按行分割
print(name.isalpha())#检查字符串是否只包含字母
print(name.isdigit())#检查字符串是否只包含数字
print(name.isalnum())#检查字符串是否只包含字母和数字
print(name.islower())#检查字符串是否全为小写,若字符串中包含非字母字符，则返回False
print(name.isupper())#检查字符串是否全为大写
print(name.isspace())#检查字符串是否只包含空白字符
print(name.isprintable())#检查字符串是否可打印
print(name.zfill(50))#数字字符串填充0到指定长度，如果字符串长度小于指定长度，则在左侧填充0，即使字符串长度达到指定长度
print(name.startswith("Ada", 0, 3))#检查字符串在指定范围内是否以指定子字符串开头
print(name.endswith("Lovelace", 0, 10))#检查字符串在指定范围内是否以指定子字符串结尾
print(name.partition("Lovelace"))#分割字符串为三部分：分隔符前、分隔符、分隔符后
print(name.rpartition("Lovelace"))#从右侧分割字符串为三部分：分隔符前、分隔符、分隔符后
print(name.split(' ', 1))#按空格分割，限制分割次数为1
print(name.join(['Hello', 'World']))#将字符串作为分隔符连接列表中的元素
print(name.translate(str.maketrans("Ada", "123")))#字符替换，'A'->'1', 'd'->'2', 'a'->'3'
print(name.format())#格式化字符串，即将字符串中的花括号替换为对应的值
print(name.format_map({'name': 'Ada Lovelace'}))#使用字典格式化字符串
print(name.removeprefix("Ada "))#移除前缀
print(name.removesuffix("Lovelace"))#移除后缀
print(name.casefold())#转换为小写，适用于更严格的比较
print(name.expandtabs(4))#将制表符转换为指定数量的空格
print(name.rfind("Lovelace"))#从右侧查找子字符串位置
print(name.rindex("Lovelace"))#从右侧查找子字符串位置，若不存在则抛出异常
print(name.isidentifier())#检查字符串是否是有效的标识符
print(name.format_spec())#获取格式化规范