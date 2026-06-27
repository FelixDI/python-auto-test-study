#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-27 10:14
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : generate_users_json.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 大量业务数据（初始化数据库、批量导入）常用格式JSON / CSV； 几乎所有 HTTP API 都使用 JSON


# 关键技巧和注意事项
# 1. 去重：避免重复数据
# 用户名、手机号、邮箱这类唯一字段，用 fake.unique.xxx() 生成，自动保证不重复。
# 生成完调用 fake.unique.clear() 可以清空已用记录。
# 通常在每个测试结束后调用 fake.unique.clear()，避免不同测试之间共享唯一值缓存。

# 2. 固定种子：复现相同数据
# 如果希望每次运行生成一模一样的数据，方便调试，加一行种子：
# Faker.seed(12345)  # 固定随机种子，每次运行结果相同（换一台电脑运行、GitHub Actions 运行，只要还是Faker.seed(12345)）
# 任意的整数，作为随机数生成器的初始种子（seed）使用，只要种子值相同，生成的随机数据就相同；种子值不同，生成的数据就不同。

# 3. 大批量生成的效率
# 生成几万条 JSON/YAML 数据，这个脚本几秒就能跑完，完全没问题；
# 如果是要往数据库灌几十万条数据，不要循环调接口，直接写 executemany 批量 SQL 插入，效率高几十倍，Faker 只负责生成字段值。
# 即不要HTTP requests.post 通过后端写数据, 直接SQL语句 cursor.executemany 写入数据库
# 实在要测写入数据库之前的大量数据 通过 Faker + Locust

# 4. 边界异常数据不要靠 Faker
# Faker 只能生成格式正常的数据，空值、超长、格式错误、业务边界值（比如超库存数量）必须手动设计，这是测试思维的核心，不能丢给工具。
# Faker只能生成合法合规的正常等价类数据，自动生成不了边界值、异常等价类。
# 正向有效等价类：可以借助 Faker 批量产出符合格式的合法参数；
# 边界值、空值、格式错误、超长字符、非法参数这类场景，Faker 无法自动构造，必须人工手动编写；
# Faker 没有内置等价类与边界值算法，不会自动区分有效 / 无效输入。
# 正常数据交给 Faker 生成，边界和异常用例手动编写，二者配合完成全量数据覆盖。

# Faker + Locust 是一个很经典的组合：Faker 负责实时生成请求数据，Locust 负责高并发发送请求。
# post_body = {
#     "username": fake.unique.user_name(),
#     "email": fake.unique.email(),
#     "age": fake.random_int(min=18, max=60)
# }


import json
from faker import Faker

# 中文本地化
fake = Faker("zh_CN")


def generate_users(count=1000):
    user_list = []
    for _ in range(count):
        # 每次循环生成 1 条完整的、字段互相关联的用户数据
        user = {
            "username": fake.unique.user_name(),  # unique 保证用户名不重复
            "phone": fake.unique.phone_number(),  # 手机号唯一
            "email": fake.unique.email(),
            "password": "Test@1234"
        }
        user_list.append(user)
    return user_list


if __name__ == "__main__":
    # 生成 1000 条用户数据
    users = generate_users(1000)

    # 写入 JSON 文件
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    print(f"成功生成 {len(users)} 条用户数据，已保存到 data/users.json")
