#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 23:45
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_unittest_demo.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : overview unittest

import unittest

# 类 + 方法，必须继承 TestCase
class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.text = "hello world"

    def tearDown(self):
        self.text = ""

    def test_upper(self):
        self.assertEqual(self.text.upper(), "HELLO WORLD")

    def test_split(self):
        result = self.text.split()
        self.assertEqual(result, ["hello", "world"])

    def test_in(self):
        self.assertIn("hello", self.text)

    def test_is_not_none(self):
        self.assertIsNotNone(self.text)

    @unittest.skip
    def test_skip(self):
        self.assertEqual(1,2)

    @unittest.skipIf(True, "条件跳过")
    def test_skip_if(self):
        pass

    def test_raise(self):
        with self.assertRaises(ValueError):
            int("abc")


class TestWithClassSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = "数据库连接"

    @classmethod
    def tearDownClass(cls):
        cls.connection = None

    def test_connection_exist(self):
        self.assertEqual(self.connection, "数据库连接")

    def test_connection_not_none(self):
        self.assertIsNotNone(self.connection)



## test_unittest_demo.py
# import unittest
#
# # ==================== 1. 基本测试类 ====================
# class TestStringMethods(unittest.TestCase):
#
#     # setUp：每个用例前执行
#     def setUp(self):
#         self.text = "hello world"
#
#     # tearDown：每个用例后执行
#     def tearDown(self):
#         self.text = ""
#
#     def test_upper(self):
#         self.assertEqual(self.text.upper(), "HELLO WORLD")
#
#     def test_split(self):
#         result = self.text.split()
#         self.assertEqual(result, ["hello", "world"])
#
#     def test_in(self):
#         self.assertIn("hello", self.text)
#
#     def test_is_not_none(self):
#         self.assertIsNotNone(self.text)
#
#     # ==================== 2. 跳过测试 ====================
#     @unittest.skip("演示跳过")
#     def test_skip(self):
#         self.assertEqual(1, 2)
#
#     @unittest.skipIf(True, "条件跳过")
#     def test_skip_if(self):
#         pass
#
#     # ==================== 3. 异常断言 ====================
#     def test_raises(self):
#         with self.assertRaises(ValueError):
#             int("abc")
#
# # ==================== 4. setUpClass / tearDownClass ====================
# class TestWithClassSetup(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.connection = "数据库连接"
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.connection = None
#
#     def test_connection_exists(self):
#         self.assertEqual(self.connection, "数据库连接")
#
#     def test_connection_not_none(self):
#         self.assertIsNotNone(self.connection)
