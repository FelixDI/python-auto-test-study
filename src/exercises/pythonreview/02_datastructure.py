#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-12 17:00
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : 02_datastructure.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : python review

nums = [1, 2, 3, 4]

nums.append(5)
nums.extend([6, 7])
nums.insert(0, 0)
print(nums.pop())
print(nums.pop(0))

nums.remove(3)
print(nums)

print(nums.index(5))
print(nums.count(2))

nums.sort(reverse=True)
# print(nums)
nums.reverse()
print(nums)

print(nums[1:3])
print(nums[::2])

squares = [i**2 for i in range(5) if i % 2 == 0]
print(squares)

point = (1, 2)
x, y = point
print(x, y)

from collections import namedtuple
User = namedtuple('User', ['name', 'age'])
u = User('张三',25)
print(u.name, u.age)

d = {'a': 1, 'b': 2}
d2 = dict(a = 1, b = 2)    # dict() 键名必须是合法的 Python 标识符（即只能包含字母、数字、下划线，且不能以数字开头）
print(d2)
print(d['a'])
print(d.get('c','缺省'))
d['c'] = 3
# print(d)
d.update({'d':4, 'e':5})
print(d)
print(d.keys())
print(d.values())
print(d.items())

val = d.setdefault('f', 0)  #setdefault() 会返回键对应的值
print(val, d)

square_map = {i:i**2 for i in range(5)}
print(square_map)

a_set = {1, 2, 3, 4}
b_set = {3, 4, 5, 6}
print(a_set)
print(b_set)
print(a_set | b_set)
print(a_set & b_set)
print(a_set - b_set)
print(a_set ^ b_set)

nums_with_dup = [1, 2, 2, 3, 3, 3]
unique = list(set(nums_with_dup))   #set() 是一个内置函数，它可以接收任何可迭代对象作为参数：
print(unique)

print(range(5))   #range() 返回的是 range 类型的对象，它是一个不可变的序列类型。
print(set(range(5)))

even_set = {x for x in range(10) if x % 2 == 0}  #取余
print(even_set)

import copy
original = [[1,2], [3,4]]     # 类似c的二维数组  访问方式arr[0][0]
# Python 列表可以混合类型
# weird = [[1, 2], "hello", 100]  # 合法

shallow = copy.copy(original)
print(original[0] is shallow[0])  # True ← 同一个对象（引用地址相同）
deep = copy.deepcopy(original)

original[0][0] = 99
print(shallow)
print(deep)

#
# # ============================================
# # 二、核心数据结构
# # ============================================
#
# # ==================== 1. 列表 list ====================
# nums = [1, 2, 3, 4]
# nums.append(5)
# nums.extend([6, 7])
# nums.insert(0, 0)           # [0,1,2,3,4,5,6,7]
# print(nums.pop())           # 7
# print(nums.pop(0))          # 0
# nums.remove(3)              # 删除值为3的第一个元素
# print(nums)                 # [1,2,4,5,6]
# print(nums.index(5))        # 3
# print(nums.count(2))        # 1
# nums.sort(reverse=True)     # 原地降序
# nums.reverse()              # 反转
# print(nums)
#
# # 切片
# print(nums[1:3])            # 从索引1到2
# print(nums[::2])            # 步长2
#
# # 列表推导式
# squares = [i**2 for i in range(5) if i % 2 == 0]  # [0,4,16]
#
# # ==================== 2. 元组 tuple ====================
# point = (1, 2)              # 不可变
# x, y = point                # 拆包
# print(x, y)
#
# # 具名元组
# from collections import namedtuple
# User = namedtuple("User", ["name", "age"])
# u = User("张三", 25)
# print(u.name, u.age)
#
# # ==================== 3. 字典 dict ====================
# d = {"a": 1, "b": 2}
# print(d["a"])               # 1
# print(d.get("c", "缺省"))   # '缺省'
# d["c"] = 3
# d.update({"d": 4, "e": 5})
# print(d.keys())             # dict_keys(['a','b','c','d','e'])
# print(d.values())           # dict_values([1,2,3,4,5])
# print(d.items())            # dict_items([('a',1),...])
#
# # setdefault：有则返回，没有则设置并返回
# val = d.setdefault("f", 0)
# print(val, d)               # 0 和新增 'f':0
#
# # 字典推导式
# square_map = {i: i**2 for i in range(3)}  # {0:0,1:1,2:4}
#
# # ==================== 4. 集合 set ====================
# a_set = {1, 2, 3, 4}
# b_set = {3, 4, 5, 6}
# print(a_set | b_set)        # 并集 {1,2,3,4,5,6}
# print(a_set & b_set)        # 交集 {3,4}
# print(a_set - b_set)        # 差集 {1,2}
# print(a_set ^ b_set)        # 对称差 {1,2,5,6}
#
# # 去重
# nums_with_dup = [1,2,2,3,3,3]
# unique = list(set(nums_with_dup))  # [1,2,3]
#
# # 集合推导式
# even_set = {x for x in range(10) if x % 2 == 0}  # {0,2,4,6,8}
#
# # ==================== 5. 深浅拷贝 ====================
# import copy
#
# # 列表内嵌列表
# original = [[1, 2], [3, 4]]
# shallow = copy.copy(original)
# deep = copy.deepcopy(original)
#
# original[0][0] = 99
# print(shallow)  # [[99, 2], [3, 4]]  受影响
# print(deep)     # [[1, 2], [3, 4]]   不受影响