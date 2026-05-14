#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-12 19:01
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : 03_controlflow.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : python review

score = 85

if score >= 90:
    level = 'A'
elif score >= 80:
    level = 'B'
else:
    level = 'c'

status = '通过'if score >= 60 else '未通过'
print(level, status)

for i in range(3):
    print(i)

count = 0
while count < 3:
    count += 1
    if count == 2:
        continue
    print(count)

for i in range(5):
    if i == 3:
        break
    print(i)
else:                # for-else / while-else循环被 break 终止 → 跳过 else 子句
    print('未break')


'''for 循环会尝试从后面的可迭代对象中取出第一个元素。
如果成功取出，就进入循环体；如果取不出（即对象为空，或者迭代器已经耗尽），
就直接跳过循环体，然后执行 else 子句（如果有的话）。
'''
for i in []:
    print(i)     #因为没东西可迭代，循环体一次都不执行
else:
    print('空循环')

it = iter([1,2,3])    # 可迭代对象：可以被遍历       迭代器：具有计数器，记录"当前走到哪了"的能力
print(next(it))      # 终端pydoc next  在Python的交互式环境（如IDLE、IPython）中， help(next)
print(next(it))

class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in CountDown(2):
    print(n)


def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print('生成器')
print(next(g))
print(next(g))
print(next(g))

squares_gen = (x**2 for x in range(6) if x % 2 == 0)
print(list(squares_gen))

try:
    num = int('abc')
except ValueError as e:
    print(e)
else:
    print('无异常')
finally:
    print('必执行')

try:
    f = open('不存在的文件')
except (IOError, OSError):
    print('文件异常')

class MyError(Exception):     #Exception 是 Python 中所有内置异常的基类（base class）
    pass

try:
    raise MyError('自定义错误')
except MyError as e:
    print(e)

try:
    raise ValueError('原始')
except ValueError as e:
    raise RuntimeError('新异常') from e
finally:
    print('执行了finally')
    # print(e)              不要试图在 finally 块中访问 except 块中绑定的异常变量 异常变量在 except 块退出后被清除。


# ============================================
# 三、控制流程与迭代
# ============================================

# ==================== 1. 条件语句 ====================
score = 85
if score >= 90:
    level = "A"
elif score >= 80:
    level = "B"
else:
    level = "C"

# 三元表达式
status = "通过" if score >= 60 else "未通过"

# ==================== 2. 循环 ====================
# for 循环
for i in range(3):
    print(i)

# while 循环
count = 0
while count < 3:
    count += 1
    if count == 2:
        continue        # 跳过当次
    print(count)        # 1, 3

# break 与循环 else
for i in range(5):
    if i == 3:
        break
    print(i)            # 0,1,2
else:
    print("未break")    # 因break跳过

for i in []:
    pass
else:
    print("空循环进入else")  # 执行

# ==================== 3. 迭代器与可迭代对象 ====================
it = iter([1, 2, 3])
print(next(it))         # 1
print(next(it))         # 2

# 自定义迭代器
class CountDown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in CountDown(2):
    print(n)            # 2, 1

# ==================== 4. 生成器 ====================
# 生成器函数
def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(next(g))          # 1

# 生成器表达式
squares_gen = (x**2 for x in range(5) if x % 2 == 0)
print(list(squares_gen))  # [0,4,16]

# ==================== 5. 异常处理 ====================
# try/except/else/finally
try:
    num = int("abc")
except ValueError as e:
    print("ValueError")
else:
    print("无异常时执行")
finally:
    print("总会执行")

# 捕获多个异常
try:
    f = open("不存在的文件")
except (IOError, OSError):
    print("文件异常")

# raise 与自定义异常
class MyError(Exception):
    pass

try:
    raise MyError("自定义错误")
except MyError as e:
    print(e)

# 异常链
try:
    raise ValueError("原始")
except ValueError as e:
    raise RuntimeError("新异常") from e

# 常用内置异常
# AssertionError, TypeError, KeyError, IndexError 等