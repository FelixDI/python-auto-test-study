#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-26 17:44
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_orders.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 订单管理测试

# 根据风险等级选择验证方式。普通业务操作（注册、登录、查询）通过接口返回验证即可；
# 涉及核心业务数据变更（下单、库存扣减）必须做接口返回 + 数据库

import pytest
import requests
import allure

@allure.feature("订单管理")
class TestOrders:

    @allure.story("创建订单")
    @allure.title("正常下单并校验库存扣减")
    def test_create_order_with_db_check(self,base_url,auth_headers,db_connection):
        product_payload = {"name":"订单商品","price":50.0,"stock":5}
        resp = requests.post(f"{base_url}/products",json=product_payload,headers=auth_headers)
        assert resp.status_code == 200
        product_id = resp.json()["id"]

        order_payload = {"product_id":product_id,"quantity":2}
        with allure.step("发送下单请求"):
            resp = requests.post(f"{base_url}/orders",json=order_payload,headers=auth_headers)
            assert resp.status_code == 200
            order_data = resp.json()
            assert order_data["total_price"] == 100.0
            assert order_data["status"] == "paid"

        with allure.step("校验数据库库存"):
            with db_connection.cursor() as cursor:
                cursor.execute("SELECT stock FROM products WHERE id=%s",(product_id))
                result = cursor.fetchone()
                assert result is not None and result["stock"] == 3


    @allure.story("创建订单")
    @allure.title("库存不足时应返回400")
    def test_create_order_insufficient_stock(self,base_url,auth_headers):
        product_payload = {"name":"稀缺商品","price":100.0,"stock":1}
        resp = requests.post(f"{base_url}/products",json=product_payload,headers=auth_headers)
        product_id = resp.json()["id"]

        order_payload = {"product_id":product_id,"quantity":10}
        with allure.step("尝试超量下单"):
            resp = requests.post(f"{base_url}/orders",json=order_payload,headers=auth_headers)
            assert resp.status_code == 400
            assert "库存不足" in resp.json()["detail"]


# # test_orders.py
# import pytest
# import requests
# import allure
#
# @allure.feature("订单管理")
# class TestOrders:
#
#     @allure.story("创建订单")
#     @allure.title("正常下单并校验库存扣减")
#     def test_create_order_with_db_check(self, base_url, auth_headers, db_connection):
#         # 1. 添加一个商品
#         product_payload = {"name": "订单商品", "price": 50.0, "stock": 5}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         # 2. 下单，购买2件
#         order_payload = {"product_id": product_id, "quantity": 2}
#         with allure.step("发送下单请求"):
#             resp = requests.post(f"{base_url}/orders", json=order_payload, headers=auth_headers)
#             assert resp.status_code == 200
#             order_data = resp.json()
#             assert order_data["total_price"] == 100.0
#             assert order_data["status"] == "paid"
#
#         # 3. 校验数据库库存
#         with allure.step("校验数据库库存"):
#             with db_connection.cursor() as cursor:
#                 cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
#                 result = cursor.fetchone()
#                 assert result is not None and result["stock"] == 3
#
#     @allure.story("创建订单")
#     @allure.title("库存不足时应返回400")
#     def test_create_order_insufficient_stock(self, base_url, auth_headers):
#         product_payload = {"name": "稀缺商品", "price": 100.0, "stock": 1}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         product_id = resp.json()["id"]
#
#         order_payload = {"product_id": product_id, "quantity": 10}
#         with allure.step("尝试超量下单"):
#             resp = requests.post(f"{base_url}/orders", json=order_payload, headers=auth_headers)
#             assert resp.status_code == 400
#             assert "库存不足" in resp.json()["detail"]

