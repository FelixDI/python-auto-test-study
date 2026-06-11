#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-11 21:15
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_order.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 订单模块测试


import pytest


@pytest.mark.smoke
def test_create_order(order_api, product_api, test_data):
    # 创建商品
    product_data = test_data["products"][0]
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]  # 数据库生成
    initial_stock = product_data["stock"]

    # 创建订单
    order_data = test_data["orders"][0]  # 包含两种订单字典列表
    response = order_api.create_order(
        product_id=product_id,
        quantity=order_data["quantity"],
    )
    # 订单成功
    order_api.assert_status_code(200)
    order_api.assert_json_contains({
        "product_id": product_id,
        "quantity": order_data["quantity"],
        "total_price": product_data["price"] * order_data["quantity"],
        "status": "paid"
    })
    order_api.assert_json_has_fields(["id", "user_id"])  # 订单id、用户id

    # 验证库存
    updated_product = product_api.get_product(product_id).json()
    assert updated_product["stock"] == initial_stock - order_data["quantity"]

def test_create_order_insufficient_stock(order_api, product_api, test_data):
    product_data = {
        "name": "库存不足的测试商品",
        "price": 100.0,
        "stock": 1
    }
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]

    # 超买
    response = order_api.create_order(
        product_id=product_id, quantity=2
    )
    order_api.assert_status_code(400)
    order_api.assert_error_message("库存不足")

def test_create_order_nonexistent_product(order_api):
    response = order_api.create_order(product_id="999999", quantity=1)
    order_api.assert_status_code(404)
    order_api.assert_error_message("商品不存在")

def test_get_order_detail(order_api, product_api, test_data):
    product_data = test_data["products"][2]
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]  # 用于下订单

    order_response = order_api.create_order(product_id=product_id, quantity=1)
    order_id = order_response.json()["id"]  # 用于查订单

    response = order_api.get_order(order_id)
    order_api.assert_status_code(200)
    order_api.assert_json_contains({
        "id": order_id,
        "product_id": product_id,
        "quantity": 1,
        "status": "paid"
    })

def test_get_nonexistent_order(order_api):
    response = order_api.get_order(999999)
    order_api.assert_status_code(404)
    order_api.assert_error_message("订单不存在")

def test_create_order_without_auth(user_api):
    response = user_api.post("/orders", json={"product_id":1, "quantity":1})

    print(response.status_code)
    print(response.json())

    user_api.assert_status_code(401)
    # user_api.assert_error_message("无法验证凭据")
    user_api.assert_error_message("Not authenticated")  # 后端没定义 无token的返回信息 fastapi默认Not authenticated


# # src/ecommerce_api_test/test_cases/test_order.py
# import pytest
#
# @pytest.mark.smoke
# def test_create_order(order_api, product_api, test_data):
#     """测试创建订单（完整流程）"""
#     # 1. 创建商品
#     product_data = test_data["products"][0]
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#     initial_stock = product_data["stock"]
#
#     # 2. 创建订单
#     order_data = test_data["orders"][0]
#     response = order_api.create_order(
#         product_id=product_id,
#         quantity=order_data["quantity"]
#     )
#
#     # 3. 断言订单创建成功
#     order_api.assert_status_code(200)
#     order_api.assert_json_contains({
#         "product_id": product_id,
#         "quantity": order_data["quantity"],
#         "total_price": product_data["price"] * order_data["quantity"],
#         "status": "paid"
#     })
#     order_api.assert_json_has_fields(["id", "user_id"])
#
#     # 4. 验证库存减少
#     updated_product = product_api.get_product(product_id).json()
#     assert updated_product["stock"] == initial_stock - order_data["quantity"]
#
# def test_create_order_insufficient_stock(order_api, product_api, test_data):
#     """测试创建订单时库存不足"""
#     # 1. 创建一个库存为1的商品
#     product_data = {
#         "name": "库存不足测试商品",
#         "price": 100.0,
#         "stock": 1
#     }
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#
#     # 2. 尝试购买2个（应该失败）
#     response = order_api.create_order(product_id=product_id, quantity=2)
#
#     order_api.assert_status_code(400)
#     order_api.assert_error_message("库存不足")
#
# def test_create_order_nonexistent_product(order_api):
#     """测试创建订单时商品不存在"""
#     response = order_api.create_order(product_id=999999, quantity=1)
#
#     order_api.assert_status_code(404)
#     order_api.assert_error_message("商品不存在")
#
# def test_get_order_detail(order_api, product_api, test_data):
#     """测试获取订单详情"""
#     # 1. 创建商品和订单
#     product_data = test_data["products"][2]
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#
#     create_order_response = order_api.create_order(product_id=product_id, quantity=1)
#     order_id = create_order_response.json()["id"]
#
#     # 2. 获取订单详情
#     response = order_api.get_order(order_id)
#
#     order_api.assert_status_code(200)
#     order_api.assert_json_contains({
#         "id": order_id,
#         "product_id": product_id,
#         "quantity": 1,
#         "status": "paid"
#     })
#
# def test_get_nonexistent_order(order_api):
#     """测试获取不存在的订单"""
#     response = order_api.get_order(999999)
#
#     order_api.assert_status_code(404)
#     order_api.assert_error_message("订单不存在")
#
# def test_create_order_without_auth(user_api):
#     """测试未认证时创建订单（应该失败）"""
#     response = user_api.post("/orders", json={"product_id": 1, "quantity": 1})
#
#     user_api.assert_status_code(401)
#     user_api.assert_error_message("无法验证凭据")