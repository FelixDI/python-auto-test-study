#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-14 15:43
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : combine45_classBaseTest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 综合练习2:定义一个基础测试类，实现用例前置 / 后置方法


class BaseTest:

    @classmethod
    def setUpClass(cls):
        print(f"\n[类前置]{cls.__name__}开始执行")

    @classmethod
    def tearDownClass(cls):
        print(f"[类后置]{cls.__name__}执行完毕\n")

    def setUp(self):
        print(" [前置]准备测试数据...")

    def tearDown(self):
        print(" [后置]清理测试数据...")

    def run(self):
        cls = type(self)              # 返回这个实例的类，即 TestLogin
        cls.setUpClass()

        for method_name in dir(self):
            if not method_name.startswith("test_"):
                continue

            method = getattr(self, method_name)      # 按字符串名称取出对象的方法
            if not callable(method):
                continue

            print(f"\n---执行用例:{method_name}---")

            try:
                self.setUp()
                method()
                self.tearDown()
            except AssertionError as e:
                print(f" ❌断言失败:{e}")
                self.tearDown()
            except Exception as e:
                print(f" 💥测试出错:{type(e).__name__}:{e}")
                self.tearDown()

        cls.tearDownClass()


class TestLogin(BaseTest):

    def test_with_valid_credentials(self):
        print(" 执行登录逻辑: admin / 123456")
        assert True,"登录成功"

    def test_with_empty_password(self):
        print(" 执行登录逻辑: admin / 空密码")
        assert False,"密码不能为空"

    def test_with_invalid_user(self):
        print(" 执行登录逻辑: invalid_user / 123456")
        try:
            raise ValueError("用户不存在")
        except ValueError:
            pass

    def test_with_exception(self):
        print(" 执行会产生除零异常")
        1/0

if __name__ == "__main__":
    suite = TestLogin()
    suite.run()


#
# ============================================
# 实战2：基础测试类（前置/后置）
# ============================================
#
# class BaseTest:
#     """所有测试用例的基类，提供 setUp / tearDown 机制"""
#
#     @classmethod
#     def setUpClass(cls):
#         """类级别前置：当前测试类只执行一次（在所有用例之前）"""
#         print(f"\n[类前置] {cls.__name__} 开始执行")
#
#     @classmethod
#     def tearDownClass(cls):
#         """类级别后置：当前测试类只执行一次（在所有用例之后）"""
#         print(f"[类后置] {cls.__name__} 执行完毕\n")
#
#     def setUp(self):
#         """实例级别前置：每个测试方法前执行"""
#         print("  [前置] 准备测试数据...")
#
#     def tearDown(self):
#         """实例级别后置：每个测试方法后执行（无论成功失败）"""
#         print("  [后置] 清理测试环境...")
#
#     def run(self):
#         """核心执行引擎：自动找到所有 test_ 开头的方法并执行"""
#         cls = type(self)          # 获取当前类（而不是实例）
#
#         cls.setUpClass()          # 1. 调用类前置
#
#         # 遍历所有属性名，找出 test_ 开头的方法
#         for method_name in dir(self):
#             if not method_name.startswith("test_"):
#                 continue
#             method = getattr(self, method_name)
#             if not callable(method):
#                 continue
#
#             print(f"\n--- 执行用例: {method_name} ---")
#             try:
#                 self.setUp()      # 2. 调用实例前置
#                 method()          # 3. 执行测试方法本身
#                 self.tearDown()   # 4. 无论是否异常都执行后置
#             except AssertionError as e:
#                 print(f"  ❌ 断言失败: {e}")
#                 self.tearDown()   # 失败也要清理
#             except Exception as e:
#                 print(f"  💥 测试出错: {type(e).__name__}: {e}")
#                 self.tearDown()
#
#         cls.tearDownClass()       # 5. 调用类后置
#
#
# # ==================== 实际测试类 ====================
# class TestLogin(BaseTest):
#     """模拟登录功能测试"""
#
#     def test_with_valid_credentials(self):
#         """正常登录：应该成功"""
#         print("    执行登录逻辑：admin / 123456")
#         # 模拟检查
#         assert True, "登录成功"
#
#     def test_with_empty_password(self):
#         """密码为空：应该返回错误"""
#         print("    执行登录逻辑：admin / 空密码")
#         # 模拟一个会失败的断言
#         assert False, "密码不能为空"
#
#     def test_with_invalid_user(self):
#         """不存在的用户：应该返回 404"""
#         print("    执行登录逻辑：invalid_user / 123456")
#         try:
#             # 模拟接口返回 404，这里用异常表示
#             raise ValueError("用户不存在")
#         except ValueError:
#             # 预期异常，测试通过
#             pass
#
#
# # ==================== 运行 ====================
# if __name__ == "__main__":
#     suite = TestLogin()
#     suite.run()