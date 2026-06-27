#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-27 11:11
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : generate_nested_json.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 数据改动少 且嵌套数据JSON更易读


# Faker("zh_CN") 并不会让所有 Provider 都生成中文数据。Faker 已经把不同类型的数据封装成不同的方法（Provider）
# Faker 已经按业务场景把数据生成规则封装好了，你调用什么方法，就生成什么类型的数据。
# Faker 已经内置了几百种 Provider，大多数业务数据都能直接生成，没必要自己造轮子。查Faker文档有没有对应的方法

# 例如 fake.user_name() fake.email() 互联网账号数据 不用中文
# fake.name()          # 张伟
# fake.address()       # 安徽省合肥市……
# fake.company()       # 北京某某科技有限公司
# fake.province()      # 安徽省
# fake.city()          # 合肥市

# Faker 的高级用法可以自定义 Provider
# 公司要求用户名格式必须是：
# AT_000001
# AT_000002
# AT_000003

# from faker import Faker
# from faker.providers import BaseProvider
#
# class MyProvider(BaseProvider):
#     def employee_id(self):
#         return f"AT_{self.generator.random_int(1, 999999):06d}"
#
# fake = Faker()
# fake.add_provider(MyProvider)
#
# print(fake.employee_id())  # AT_000123

import json
from faker import Faker

fake = Faker("zh_CN")

def generate_orders(count=500):
    order_list = []
    for _ in range(count):
        order = {
            "order_no": fake.uuid4(),  # 测试数据用faker.uuid4() 直接返回字符串；业务代码用uuid.uuid4()（通常UUID对象必须str()）
            "product_id": fake.random_int(min=1, max=100),
            "quantity": fake.random_int(min=1, max=5),
            "receiver": {  # 嵌套的收货地址结构
                "name": fake.name(),
                "phone": fake.phone_number(),
                "address": fake.address(),
                "postcode": fake.postcode()
            },
            "create_time": fake.date_time_this_year().isoformat()
        }
        order_list.append(order)
    return order_list

if __name__ == "__main__":
    orders = generate_orders(500)
    with open("data/orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    print(f"生成 {len(orders)} 条订单数据")