#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 16:51
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : db_util.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 封装 MySQL 连接和基本操作 只负责数据库操作


import pymysql

from typing import Optional, Dict, List, Tuple


class DBUtil:
    """
    数据库工具类
    """

    def __init__(
            self,
            host: str,
            port: int = 3306,
            user: str = "root",
            password: str = "root123",
            database: str = "ecommerce"
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn: Optional[pymysql.Connection] = None

    # func()普通方法 _func()内部方法  __func()私有方法  __xxx__魔术方法(Python内置机制)
    # __enter__ + __exit__ 就是让类支持 with 语句，实现“自动资源管理”（连接自动打开，用完自动关闭）。
    # from __future__ import annotations
    def __enter__(self) -> "DBUtil":
        self.connect()
        return self

    # exc_type = 异常类型
    # exc_val  = 异常内容
    # exc_tb   = 堆栈信息
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if not self.conn or not self.conn.open:  # 如果：还没有连接（self.conn 是 None）或连接已经断了（conn.open = False）
            # TCP 连接 mysql
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4",  # 支持中文、emoji
                cursorclass = pymysql.cursors.DictCursor,  # 默认tuple 这里设置游标查询结果返回 dict
                autocommit=False  # 关闭自动提交，手动控制事务self.conn.commit()  插入数据 → 测试接口 → 回滚/清理
            )

    def close(self):
        if self.conn and self.conn.open:
            self.conn.close()  # pymysql
            self.conn = None

    # 查询封装层
    def query_one(self, sql: str, params: Tuple = None) -> Optional[Dict]:
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)  # 防 SQL 注入,params 会把输入“强制当作普通字符串处理”，不会让它参与 SQL 语法解析
            return cursor.fetchone()

    # pymysql 的 execute 方法会把 ' OR '1'='1 这个完整字符串当作一个普通数据，安全地填充到 %s 占位符里。
    # SQL 语句里用 %s 占位符，参数用元组传进去，就是安全的. cursor.execute("SELECT * FROM products WHERE price > %s", (5000,))
    def query_all(self, sql: str, params: Tuple = None) -> List[Dict]:
        # 创建游标
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)  # cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

    # DBUtil “写操作层”：负责 INSERT / UPDATE / DELETE
    def execute(self, sql: str, params: Tuple = None) -> int:
        with self.conn.cursor() as cursor:
            affected_rows = cursor.execute(sql, params)  # 执行sql语句
            self.conn.commit()  # 写入数据库
            return affected_rows

    def execute_many(self, sql: str, params_list: List[Tuple]) -> int:
        with self.conn.cursor() as cursor:
            # execute 用于单条写操作，executemany 用于批量写操作，两者都会返回影响行数
            affected_rows = cursor.executemany(sql, params_list)
            self.conn.commit()
            return affected_rows


# # src/ecommerce_api_test/utils/db_util.py
# import pymysql
# from typing import Optional, Dict, List, Tuple
#
# class DBUtil:
#     """
#     数据库工具类，封装 MySQL 连接和基本操作
#     保持纯粹：只负责数据库操作，不处理环境配置
#     所有配置由外部注入
#     """
#
#     def __init__(
#         self,
#         host: str,
#         port: int = 3306,
#         user: str = "root",
#         password: str = "root123",
#         database: str = "ecommerce",
#     ):
#         self.host = host
#         self.port = port
#         self.user = user
#         self.password = password
#         self.database = database
#         self.conn: Optional[pymysql.Connection] = None
#
#     def __enter__(self) -> "DBUtil":
#         """支持 with 语句，自动建立连接"""
#         self.connect()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """退出 with 语句时自动关闭连接"""
#         self.close()
#
#     def connect(self):
#         """建立数据库连接"""
#         if not self.conn or not self.conn.open:
#             self.conn = pymysql.connect(
#                 host=self.host,
#                 port=self.port,
#                 user=self.user,
#                 password=self.password,
#                 database=self.database,
#                 charset="utf8mb4",
#                 cursorclass=pymysql.cursors.DictCursor,
#                 autocommit=False  # 关闭自动提交，手动控制事务
#             )
#
#     def close(self):
#         """关闭数据库连接"""
#         if self.conn and self.conn.open:
#             self.conn.close()
#             self.conn = None
#
#     def query_one(self, sql: str, params: Tuple = None) -> Optional[Dict]:
#         """执行查询并返回第一条结果"""
#         with self.conn.cursor() as cursor:
#             cursor.execute(sql, params)
#             return cursor.fetchone()
#
#     def query_all(self, sql: str, params: Tuple = None) -> List[Dict]:
#         """执行查询并返回全部结果"""
#         with self.conn.cursor() as cursor:
#             cursor.execute(sql, params)
#             return cursor.fetchall()
#
#     def execute(self, sql: str, params: Tuple = None) -> int:
#         """执行增删改操作，返回影响行数"""
#         with self.conn.cursor() as cursor:
#             affected_rows = cursor.execute(sql, params)
#             self.conn.commit()
#             return affected_rows
#
#     def execute_many(self, sql: str, params_list: List[Tuple]) -> int:
#         """批量执行增删改操作"""
#         with self.conn.cursor() as cursor:
#             affected_rows = cursor.executemany(sql, params_list)
#             self.conn.commit()
#             return affected_rows