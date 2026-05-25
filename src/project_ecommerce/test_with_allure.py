#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-25 19:17
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_with_allure.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : learn allure

import pytest
import allure

@allure.feature("用户管理")
@allure.story("用户查询")
@allure.title("查询所有用户并验证数据不为空")
def test_get_all_users(db_connection):
    with allure.step("步骤1:执行SQL查询所有用户"):
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

    with allure.step("步骤2:验证查询结果不为空"):
        assert len(users)>0,"用户表为空"

    with allure.step("步骤3:验证返回字段完整性"):
        user=users[0]
        assert "id" in user
        assert "username" in user
        assert "email" in user

    allure.attach(
        str(users),
        name="用户列表数据",
        attachment_type=allure.attachment_type.TEXT
    )



@allure.feature("商品管理")
@allure.story("商品查询")
@allure.title("查询价格大于5000的商品")
def test_get_expensive_products(db_connection):
    with allure.step("步骤1:执行参数化查询"):
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE price>%s",(5000,))
            products = cursor.fetchall()

    with allure.step("步骤2:验证每个商品价格都大于5000"):
        for product in products:
            assert product["price"]>5000,\
            f"商品 {product["id"]}价格 {product["price"]}不大于5000"

    allure.attach(
        str(products),
        name="高价商品列表",
        attachment_type=allure.attachment_type.TEXT
    )


@allure.feature("商品管理")
@allure.story("商品查询")
@allure.title("故意失败的用例————演示Allure报告中的失败截图")
def test_intentional_fail():
    with allure.step("执行一个必然失败的断言"):
        assert 1 == 2,"故意失败的断言，用于演示Allure失败报告"