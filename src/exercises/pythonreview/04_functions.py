#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-13 11:06
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : 04_functions.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : python review


def add(a, b):
    return a + b

print(add(1, 2))

def get_user_info():
    return "admin", "admin@test.com"

name, email = get_user_info()
print(name, email)


def request(method='GET', url='/', body = None):
    print(f"{method}{url}body={body}")

request("POST", "/login", {"pwd":"123"})
request()

def log(*messages):
    print("|".join(messages))

log("INFO", "test_start", "passed")

def build_request(**kwargs):
    print(kwargs)

build_request(method="GET", url="/api", timeout=5)


# 强制关键字参数（*）和参数解包（* / **）  函数定义中的 * 不是收集参数，只起分隔作用
# * 后面的所有参数（这里是 timeout）必须使用关键字参数传递
def connect(host, *, timeout=10):
    print(host, timeout)

connect("localhost", timeout=5)

params = [1, 2]
add(*params)
opts= {"timeout":20}
connect("localhost", **opts)


x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)

    inner()

outer()

def counter(start=0):
    count = [start]

    def inc():
        count[0] += 1

        return count[0]

    return inc     # 返回一个函数

c = counter(10)
print(c())
print(c())


nums = [1, 2, 3, 4]
doubled = list(map(lambda x:x*2, nums))    # lambda + 表达式

print(doubled)

pairs = [(1, "bbb"),(3, "aaa"),(2, "ccc")]
pairs.sort(key=lambda p:p[1])
# key=lambda + 表达式  凡是涉及"比较大小/确定顺序"的函数或方法，通常都会有 key 参数，用来指定"按什么比较"
print(pairs)

#
# 简单来说：**装饰器让你在不改动原函数代码的情况下，给函数“穿衣服”**。复杂场景下的便利主要体现在：
# 1. **避免重复代码**
#    如果很多函数都需要日志、计时、权限校验，每个函数里都写一遍相同的 `print("调用...")` 会非常冗余。
#    装饰器把公共功能抽出来，用 `@` 一行附加到任意函数上。
# 2. **分离核心逻辑与辅助逻辑**
#    原函数只关心业务（比如 `add` 只做加法），日志、缓存、鉴权等辅助功能交给装饰器。代码更清晰，也更容易单独测试。
# 3. **灵活组合与叠加**
#    可以给一个函数加上多个装饰器（例如 `@log`、`@cache`、`@auth`），并且可以随时增删、调整顺序，不需要修改原函数内部。
# 4. **运行时动态增强**
#    比如根据配置文件决定是否启用缓存，或者为不同环境（开发/生产）挂上不同的装饰器。这比硬编码在原函数里灵活得多。
# 5. **保持接口一致**
#    装饰器包装后的函数签名、返回值与原函数一致（`functools.wraps` 帮忙），调用方无需知道它是否被增强。

# 一个典型复杂场景：
# - 你有 50 个函数需要添加**执行时间统计** + **Redis 缓存** + **权限校验**。
# - 不用装饰器：50 个函数里每个都要写十几行重复代码，维护时改一处要改 50 处。
# - 用装饰器：定义 `@timer`、`@cache`、`@permission`，然后在每个函数上面叠加即可。哪天不想缓存了，删掉 `@cache` 一行就行。

# **核心优势：开闭原则（对扩展开放，对修改封闭）——不修改原函数，却能增加新功能。**

import functools

def log_func(func):
    # 把 wrapper 的元信息（如 __name__）改成原 add 的
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用{func.__name__},args={args},kwargs={kwargs}")  #使用add()的属性
        result = func(*args, **kwargs)                             #使用add()的功能代码
        print(f"返回{result}")

        return result  #好的装饰器应该不破坏原函数的功能：原函数有返回值 → 装饰器也要返回
                        # 原函数无返回值 → 装饰器返回 None 即无返回值（隐式 return None）
    return wrapper       # 新的 add 是一个有日志打印功能的包装函数

# 语法糖生效，相当于执行 add = log_func(add)
@log_func
def add(a, b):
    return a + b

add(2, 3)


def mark(tag):
    def decorator(func):
        func.tag = tag
        return func
    return decorator

@mark("smoke")
def test_login():
    pass

print(test_login.tag)


# # ============================================
# # 四、函数
# # ============================================
#
# # ==================== 1. 定义与调用 / 多值返回 ====================
# def add(a, b):
#     return a + b
#
# print(add(1, 2))
#
# def get_user_info():
#     return "admin", "admin@test.com"   # 返回元组
#
# name, email = get_user_info()
# print(name, email)
#
# # ==================== 2. 参数传递 ====================
# # 默认参数
# def request(method="GET", url="/", body=None):
#     print(f"{method} {url} body={body}")
#
# request("POST", "/login", {"pwd": "123"})
# request()  # 使用默认值
#
# # 可变位置参数 *args
# def log(*messages):
#     print(" | ".join(messages))
#
# log("INFO", "test_start", "passed")
#
# # 可变关键字参数 **kwargs
# def build_request(**kwargs):
#     print(kwargs)
#
# build_request(method="GET", url="/api", timeout=5)
#
# # 仅限关键字参数
# def connect(host, *, timeout=10):
#     print(host, timeout)
#
# connect("localhost", timeout=5)
#
# # 参数解包
# params = [1, 2]
# add(*params)           # 解包列表
# opts = {"timeout": 20}
# connect("localhost", **opts)
#
# # ==================== 3. 作用域与闭包 ====================
# x = "global"
#
# def outer():
#     x = "enclosing"
#     def inner():
#         # nonlocal x   # 若修改外层变量需声明
#         print(x)       # 查找 outer 内的 x
#     inner()
#
# outer()                 # enclosing
#
# # 闭包典型用法——保存状态
# def counter(start=0):
#     count = [start]     # 列表可变，可修改
#     def inc():
#         count[0] += 1
#         return count[0]
#     return inc
#
# c = counter(10)
# print(c())  # 11
# print(c())  # 12
#
# # ==================== 4. 匿名函数 lambda ====================
# nums = [1, 2, 3, 4]
# doubled = list(map(lambda x: x * 2, nums))
# print(doubled)  # [2,4,6,8]
#
# # 常用于排序键
# pairs = [(1, "bbb"), (3, "aaa"), (2, "ccc")]
# pairs.sort(key=lambda p: p[1])
# print(pairs)    # [(3,'aaa'),(1,'bbb'),(2,'ccc')]
#
# # ==================== 5. 装饰器 ====================
# import functools
#
# # 不带参数的装饰器——日志示例
# def log_func(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"调用 {func.__name__}, args={args}, kwargs={kwargs}")
#         result = func(*args, **kwargs)
#         print(f"返回 {result}")
#         return result
#     return wrapper
#
# @log_func
# def add(a, b):
#     return a + b
#
# add(2, 3)  # 自动打印日志
#
# # 带参数的装饰器——标记用例
# def mark(tag):
#     def decorator(func):
#         func.tag = tag
#         return func
#     return decorator
#
# @mark("smoke")
# def test_login():
#     pass
#
# print(test_login.tag)  # "smoke"