#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-11 13:10
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : 01_variables.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : python review

x = 10
x = 'hello'

a = 5
b = 2.0
c = 3 + 4j
print(7/3)
print(7//3)
print(7%3)
print(2**3)

t, f = True, False
print(t and f)
print(t or f)
print(not t)

s1 = '单引号'
s2 = "双引号"
s3 = """三引号
跨行"""
raw = r"原始\n不转义"

val = None
print(val is None)

print(int('123'))
print(bool(""))
print(bool('x'))

#字符串操作
name = 'test'
uid = 10086
print(f"/api/user/{uid}?name={name}")

print('a,b,c'.split(','))
print("l".join(['x','y']))

print(' hi\n'.strip())

print('Hello{who}'.replace('{who}','World'))
print('timeout'.find('out'))

print('error.log'.endswith('.log'))
print('OK'.lower())

print(1==1,2!=3,5>2)
print('a' in ['a','b'])
print('x' not in 'text')

a_list = []
b_list = a_list
print(a_list is b_list)
print([] is [])

print(len('abc'))
print(type(42))
print(isinstance('x', str))
print(range(3))

for i, v in enumerate(['a','b']):
    print(i, v)

names = ['Bob', 'Amy', 'Coco']
ages = [25, 30, 22]
for n, a in zip(names, ages):
    print(n, a)

print(sorted([3,1,2]))
print(list(reversed([3,1,2])))

# # ============================================
# # 1. 变量与基本数据类型
# # ============================================
# # 动态类型
# x = 10
# x = "hello"
#
# # 数字
# a = 5               # int
# b = 2.0             # float
# c = 3 + 4j          # complex
# print(7 / 3)        # 2.333...
# print(7 // 3)       # 2
# print(7 % 3)        # 1
# print(2 ** 3)       # 8
#
# # 布尔
# t, f = True, False
# print(t and f)      # False
# print(t or f)       # True
# print(not t)        # False
#
# # 字符串
# s1 = '单引号'
# s2 = "双引号"
# s3 = """三引号跨行"""
# raw = r"原始\n不转义"
#
# # None
# val = None
# print(val is None)  # True
#
# # 类型转换
# print(int("123"))   # 123
# print(bool(""))     # False
# print(bool("x"))    # True
#
# # ============================================
# # 2. 字符串操作
# # ============================================
# name = "test"
# uid = 10086
# # f-string
# print(f"/api/user/{uid}?name={name}")
# # split / join
# print("a,b,c".split(","))
# print("|".join(["x", "y"]))
# # strip
# print("  hi \n".strip())
# # replace
# print("Hello {who}".replace("{who}", "World"))
# # find
# print("timeout".find("out"))   # 4
# # startswith / endswith
# print("error.log".endswith(".log"))
# # upper / lower
# print("OK".lower() == "ok")
#
# # ============================================
# # 3. 运算符
# # ============================================
# # 比较
# print(1 == 1, 2 != 3, 5 > 2)
# # 成员
# print("a" in ["a", "b"])   # True
# print("x" not in "text")   # False
# # 身份
# a_list = []
# b_list = a_list
# print(a_list is b_list)    # True
# print([] is [])            # False（不同对象）
#
# # ============================================
# # 4. 常用内置函数
# # ============================================
# print(len("abc"))                  # 3
# print(type(42))                    # <class 'int'>
# print(isinstance("x", str))       # True
# print(range(3))                    # range(0, 3)
# for i, v in enumerate(["a","b"]):
#     print(i, v)                    # 0 a, 1 b
# names = ["Bob", "Amy", "Coco"]
# ages = [25, 30, 22]
# for n, a in zip(names, ages):
#     print(n, a)
# print(sorted([3, 1, 2]))          # [1, 2, 3]
# print(list(reversed([3, 1, 2])))  # [2, 1, 3]
