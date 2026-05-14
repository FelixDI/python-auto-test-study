#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-14 10:17
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : 05_OOPaboutclass.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : python review

class TestCase:
    default_timeout = 10

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.status = "not run"

    def run(self):
        self.status = "passed"
        print(f"运行用例:{self.name}->{self.status}")


tc1 = TestCase("test_login","正常登录测试")
tc1.run()
print(tc1.status, tc1.default_timeout)


class BasePage:
    def __init__(self):
        self.public_var = "公开"
        self._protected_var = "受保护"
        self.__private_var = "私有"

    def _protected_method(self):
        return "内部使用"

    def __private_method(self):
        return "不可直接访问"


p = BasePage()
print(p.public_var)
print(p._protected_var)
# print(p.__private_var)
print(p._BasePage__private_var)

class User:
    # 实例调用类的时候 u = User("张三") ，才会执行初始化
    def __init__(self, name):
        self._name = name
# 核心原则：先用普通属性，一旦发现需要校验/日志/计算属性时，立即重构为 property。Python 可以无缝切换（外部使用方无需修改代码）。
#     @property装饰器返回的是一个property对象，这个对象有三个方法：
#     getter - 获取一个getter装饰器
#     setter - 获取一个setter装饰器
#     deleter - 获取一个deleter装饰器
    @property
    def name(self):
        return self._name

# setter设置器/赋值器      完成修改name的功能
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("名字不能为空")
        self._name = value

# 装饰器就是为了可以随时增加功能，方便更改代码，而不用牵一发而动全身

u = User("张三")    # 调用 __init__，执行初始化
print(u.name)
u.name = "李四"  # # 不调用 __init__，调用 setter 完成修改
print(u.name)
# u.name = ""      # 业务需求：用户名不能为空，不能重复，长度限制等  要防止脏数据进入数据库

class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

for a in [Dog(), Cat()]:
    print(a.speak())

class TestBase:
    def setUp(self):
        print("基础 setUp")

class MyTest(TestBase):
    def setUp(self):
        super().setUp()
        print("子类 setUp")

MyTest().setUp()

class A:
    def method(self):
        print("A")

class B:
    def method(self):
        print("B")

class C(A,B):
    pass

C().method()

class TestData:
    base_url = "http://test.server"
# Python 内置的装饰器 @property @classmethod @staticmethod
#     设计目的就是服务于面向对象编程：
#     @property：控制实例属性的访问，必须在类中定义
#     @classmethod：操作类级别的数据，第一个参数是类本身
#     @staticmethod：将与类相关的工具函数放在类命名空间中
    @classmethod
    def build_url(cls, endpoint):
        return f"{cls.base_url}{endpoint}"

    @staticmethod
    def is_valid_status(code):
        return 200 <= code < 300

print(TestData.build_url("/api"))
print(TestData.is_valid_status(200))

# 自定义类 重写部分方法   展示了python语言中类的特殊方法的自由改写
class TestResult:
    # 构造函数 完成初始化  用于传参
    def __init__(self, name, passed):
        self.name = name
        self.passed = passed

    def __str__(self):
        return f"{self.name}:{'PASS' if self.passed else 'FAIL'}"

    def __repr__(self):
        return f"TestResult(name={self.name},passed={self.passed})"   #__repr__ 方法返回的是对象的 "官方字符串表示"

    def __eq__(self, other):
        return self.name == other.name and self.passed == other.passed

    def __len__(self):
        return 1

    def __call__(self):
        print(f"重放:{self}")

r1 = TestResult("test_login", True)
r2 = TestResult("test_login", True)
print(r1)
print(repr(r1))
print(r1 == r2)
print(len(r1))
r1()

class TemporaryFile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"创建临时文件:{self.name}")
        return self

    def __exit__(self, *args):
        print(f"清理临时文件:{self.name}")

with TemporaryFile("temp.txt") as f:
    print("使用文件")

from abc import ABC, abstractmethod

class BaseTest(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

class LoginTest(BaseTest):
    def run(self):
        print("执行登录测试")

    def cleanup(self):
        print("清理登录数据")

# bt = BaseTest()   # 抽象基类 不能实例化
lt = LoginTest()
lt.run()
lt.cleanup()


# # ============================================
# # 五、面向对象编程（OOP）
# # ============================================
#
# # ==================== 1. 类与实例 ====================
# class TestCase:
#     """模拟一个最简测试用例类"""
#     # 类变量（所有实例共享）
#     default_timeout = 10
#
#     def __init__(self, name, description):
#         # 实例变量
#         self.name = name
#         self.description = description
#         self.status = "not run"
#
#     def run(self):
#         """实例方法"""
#         self.status = "passed"
#         print(f"运行用例: {self.name} -> {self.status}")
#
#
# tc1 = TestCase("test_login", "正常登录测试")
# tc1.run()
# print(tc1.status, tc1.default_timeout)
#
# # ==================== 2. 访问控制 ====================
# class BasePage:
#     def __init__(self):
#         self.public_var = "公开"
#         self._protected_var = "受保护"    # 约定
#         self.__private_var = "私有"       # 名称改写
#
#     def _protected_method(self):
#         return "内部使用"
#
#     def __private_method(self):
#         return "不可直接访问"
#
#
# p = BasePage()
# print(p.public_var)
# print(p._protected_var)              # 能访问，但不推荐
# # print(p.__private_var)             # AttributeError
# print(p._BasePage__private_var)      # 强制访问（名称改写规则）
#
# # @property 装饰器
# class User:
#     def __init__(self, name):
#         self._name = name
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, value):
#         if not value:
#             raise ValueError("名字不能为空")
#         self._name = value
#
#
# u = User("张三")
# print(u.name)
# u.name = "李四"
# # u.name = ""   # ValueError
#
# # ==================== 3. 继承与多态 ====================
# class Animal:
#     def speak(self):
#         return "..."
#
# class Dog(Animal):
#     def speak(self):                # 重写
#         return "Woof"
#
# class Cat(Animal):
#     def speak(self):
#         return "Meow"
#
# # 多态：同一接口，不同行为
# for a in [Dog(), Cat()]:
#     print(a.speak())                # Woof, Meow
#
# # super() 调用父类
# class TestBase:
#     def setUp(self):
#         print("基础 setUp")
#
# class MyTest(TestBase):
#     def setUp(self):
#         super().setUp()             # 先调父类
#         print("子类 setUp")
#
# MyTest().setUp()
#
# # 多继承
# class A:
#     def method(self):
#         print("A")
#
# class B:
#     def method(self):
#         print("B")
#
# class C(A, B):  # MRO: C -> A -> B
#     pass
#
# C().method()  # A（先找到 A 的 method）
#
# # ==================== 4. 类方法与静态方法 ====================
# class TestData:
#     base_url = "http://test.server"
#
#     @classmethod
#     def build_url(cls, endpoint):
#         """类方法：可访问类变量，常用于工厂方法"""
#         return f"{cls.base_url}{endpoint}"
#
#     @staticmethod
#     def is_valid_status(code):
#         """静态方法：纯工具函数，无需访问类/实例"""
#         return 200 <= code < 300
#
#
# print(TestData.build_url("/api"))
# print(TestData.is_valid_status(200))
#
# # ==================== 5. 魔法方法 ====================
# class TestResult:
#     def __init__(self, name, passed):
#         self.name = name
#         self.passed = passed
#
#     def __str__(self):
#         return f"{self.name}: {'PASS' if self.passed else 'FAIL'}"
#
#     def __repr__(self):
#         return f"TestResult(name='{self.name}', passed={self.passed})"
#
#     def __eq__(self, other):
#         return self.name == other.name and self.passed == other.passed
#
#     def __len__(self):
#         return 1  # 一个结果对象长度为1
#
#     def __call__(self):
#         print(f"重放: {self}")
#
#
# r1 = TestResult("test_login", True)
# r2 = TestResult("test_login", True)
# print(r1)                   # test_login: PASS (__str__)
# print(repr(r1))             # TestResult(...)   (__repr__)
# print(r1 == r2)             # True              (__eq__)
# print(len(r1))              # 1                 (__len__)
# r1()                        # 重放: ...        (__call__)
#
# # 上下文管理器
# class TemporaryFile:
#     def __init__(self, name):
#         self.name = name
#
#     def __enter__(self):
#         print(f"创建临时文件: {self.name}")
#         return self
#
#     def __exit__(self, *args):
#         print(f"清理临时文件: {self.name}")
#
# with TemporaryFile("temp.txt") as f:
#     print("使用文件")
#
# # ==================== 6. 抽象基类 ====================
# from abc import ABC, abstractmethod
#
# class BaseTest(ABC):
#     @abstractmethod
#     def run(self):
#         pass
#
#     @abstractmethod
#     def cleanup(self):
#         pass
#
# class LoginTest(BaseTest):
#     def run(self):
#         print("执行登录测试")
#
#     def cleanup(self):
#         print("清理登录数据")
#
# # bt = BaseTest()  # TypeError，不能实例化抽象类
# lt = LoginTest()
# lt.run()
# lt.cleanup()

