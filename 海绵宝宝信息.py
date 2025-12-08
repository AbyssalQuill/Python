Haimian = {'name': '海绵宝宝','work': '厨师', 'age': 20,'hobby': '抓水母',
'好朋友': {'派大星': {'name': '派大星','work': '无业游民','age': 22,'hobby': '吃东西'},
'章鱼哥': {'name': '章鱼哥','work': '收银员','age': 30,'hobby': '吹小号'}}}

print('海绵宝宝的信息如下：')
for key in Haimian:
    if key != '好朋友':
        print(f'{key}：{Haimian[key]}')
    else:
        print('好朋友：')
        for friend in Haimian['好朋友']:
            print(f'  {friend}的信息如下：')
            for k in Haimian['好朋友'][friend]:
                print(f'{k}：{Haimian["好朋友"][friend][k]}')
print('快来认识海绵宝宝和他的好朋友们吧！')