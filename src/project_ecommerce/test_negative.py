#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-26 19:50
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_negative.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 负向测试

import pytest
import requests
import allure

import time


# xfail 的双刃剑——它会掩盖所有失败，包括代码写错

@allure.feature("异常流测试")
class TestNegativeScenario:

    @allure.story("注册异常")
    @allure.title("重复用户名注册应返回400")
    def test_register_duplicate_username(self,base_url):
        unique_id = int(time.time_ns())
        username = f"dup_{unique_id}"
        payload = {"username":username,"password":"123456","email":f"dup_{unique_id}@test.com"}

        with allure.step("第一次注册"):
            resp = requests.post(f"{base_url}/register",json=payload)
            assert resp.status_code == 200

        with allure.step("第二次注册（重复）"):
            resp = requests.post(f"{base_url}/register",json=payload)
            assert resp.status_code == 400
            assert "用户名已注册" in resp.json()["detail"]

    @allure.story("注册异常")
    @allure.title("重复邮箱注册应返回400（已知缺陷，目前返回500）")
    @pytest.mark.xfail(reason="已知缺陷：后端未校验邮箱唯一，触发数据库约束返回500")
    def test_register_duplicate_email(self,base_url):
        unique_id = int(time.time_ns())
        username_a = f"user_a_{unique_id}"
        username_b = f"user_b_{unique_id}"
        email = f"dupemail_{unique_id}@test.com"

        with allure.step("第一个用户注册"):
            resp = requests.post(f"{base_url}/register",json={
                "username":username_a,"password":"123456","email":email
            })

            assert resp.status_code == 200

        with allure.step("第二个用户使用相同邮箱"):
            resp = requests.post(f"{base_url}/register",json={
                "username":username_b,"password":"123456","email":email
            })

            assert resp.status_code == 400



    @allure.story("商品异常")
    @allure.title("价格为负数应拒绝（已知缺陷，当前返回200）")
    @pytest.mark.xfail(reason="已知缺陷：后端未校验负数价格，返回200")
    def test_product_negative_price(self,base_url,auth_headers):
        payload = {"name":"负价格商品","price":-999.0,"stock":10}
        with allure.step("发送负数价格请求"):
            resp = requests.post(f"{base_url}/products",json=payload,headers=auth_headers)
            assert resp.status_code == 422


    @allure.story("商品异常")
    @allure.title("库存为负数应拒绝（已知缺陷，当前返回200）")
    @pytest.mark.xfail(reason="已知缺陷：后端未校验负数库存，返回200")
    def test_product_negative_stock(self,base_url,auth_headers):
        payload = {"name":"负库存商品","price":100.0,"stock":-1}
        with allure.step("发送负数库存请求"):
            resp = requests.post(f"{base_url}/products",json=payload,headers=auth_headers)
            assert resp.status_code == 422



    @allure.story("订单异常")
    @allure.title("购买数量为负数应拒绝（已知缺陷，当前返回200）")
    @pytest.mark.xfail(reason="已知缺陷：后端未校验负数购买数量，返回200")
    def test_order_negative_quantity(self,base_url,auth_headers):
        product_payload = {"name":"正常商品","price":50.0,"stock":10}
        resp = requests.post(f"{base_url}/products",json=product_payload,headers=auth_headers)
        assert resp.status_code == 200
        product_id = resp.json()["id"]

        with allure.step("发送负数数量下单"):
            resp = requests.post(f"{base_url}/orders",json={
                "product_id":product_id,"quantity":-1
            },headers=auth_headers)

            assert resp.status_code == 422

    @allure.story("订单异常")
    @allure.title("超卖场景————库存不足应返回400")
    def test_order_oversell(self,base_url,auth_headers):
        product_payload = {"name":"限量商品","price":100.0,"stock":3}
        resp = requests.post(f"{base_url}/products",json=product_payload,headers=auth_headers)
        assert resp.status_code == 200
        product_id = resp.json()["id"]

        with allure.step("尝试购买超过库存的数量"):
            resp = requests.post(f"{base_url}/orders",json={
                "product_id":product_id,"quantity":10
            },headers=auth_headers)
            assert resp.status_code == 400
            assert "库存不足" in resp.json()["detail"]

    @allure.story("订单异常")
    @allure.title("未授权访问————不带Token下单应返回")
    def test_order_unauthorized(self,base_url):
        with allure.step("不带Token发送下单请求"):
            resp = requests.post(f"{base_url}/orders",json={
                "product_id":1,"quantity":1
            })
            assert resp.status_code == 401

# # test_negative.py
# import pytest
# import requests
# import time
# import allure
#
# @allure.feature("异常流测试")
# class TestNegativeScenarios:
#
#     # ==================== 用户注册异常 ====================
#
#     @allure.story("注册异常")
#     @allure.title("重复用户名注册应返回 400")
#     def test_register_duplicate_username(self, base_url):
#         """重复注册相同用户名，预期返回 400"""
#         unique_id = int(time.time_ns())
#         username = f"dup_{unique_id}"
#         payload = {"username": username, "password": "123456", "email": f"dup_{unique_id}@test.com"}
#
#         with allure.step("第一次注册"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 200
#
#         with allure.step("第二次注册（重复）"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 400
#             assert "用户名已注册" in resp.json()["detail"]
#
#     @allure.story("注册异常")
#     @allure.title("重复邮箱注册应返回 400（已知缺陷，目前返回 500）")
#     @pytest.mark.xfail(reason="已知缺陷：后端未校验邮箱唯一，触发数据库约束返回500")
#     def test_register_duplicate_email(self, base_url):
#         """重复邮箱触发数据库 UNIQUE 约束，预期返回 400，实际返回 500（已提交缺陷）"""
#         unique_id = int(time.time_ns())
#         username_a = f"user_a_{unique_id}"
#         username_b = f"user_b_{unique_id}"
#         email = f"dupemail_{unique_id}@test.com"
#
#         with allure.step("第一个用户注册"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_a, "password": "123456", "email": email
#             })
#             assert resp.status_code == 200
#
#         with allure.step("第二个用户使用相同邮箱"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_b, "password": "123456", "email": email
#             })
#             # 预期后端返回 400，但当前缺少邮箱校验，直接落库报 500
#             assert resp.status_code == 400
#
#     # ==================== 商品管理异常 ====================
#
#     @allure.story("商品异常")
#     @allure.title("价格为负数应拒绝（已知缺陷，当前返回 200）")
#     @pytest.mark.xfail(reason="已知缺陷：后端未校验负数价格，返回200")
#     def test_product_negative_price(self, base_url, auth_headers):
#         """商品价格不能为负数，预期 422，实际后端未校验"""
#         payload = {"name": "负价格商品", "price": -999.0, "stock": 10}
#         with allure.step("发送负数价格请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             assert resp.status_code == 422
#
#     @allure.story("商品异常")
#     @allure.title("库存为负数应拒绝（已知缺陷，当前返回 200）")
#     @pytest.mark.xfail(reason="已知缺陷：后端未校验负数库存，返回200")
#     def test_product_negative_stock(self, base_url, auth_headers):
#         """商品库存不能为负数，预期 422，实际后端未校验"""
#         payload = {"name": "负库存商品", "price": 100.0, "stock": -1}
#         with allure.step("发送负数库存请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             assert resp.status_code == 422
#
#     # ==================== 订单管理异常 ====================
#
#     @allure.story("订单异常")
#     @allure.title("购买数量为负数应拒绝（已知缺陷，当前返回 200）")
#     @pytest.mark.xfail(reason="已知缺陷：后端未校验负数购买数量，返回200")
#     def test_order_negative_quantity(self, base_url, auth_headers):
#         """下单数量不能为负数，预期 422，实际后端未校验"""
#         product_payload = {"name": "正常商品", "price": 50.0, "stock": 10}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("发送负数数量下单"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": -1
#             }, headers=auth_headers)
#             assert resp.status_code == 422
#
#     @allure.story("订单异常")
#     @allure.title("超卖场景——库存不足应返回 400")
#     def test_order_oversell(self, base_url, auth_headers):
#         """购买数量大于库存，预期返回 400"""
#         product_payload = {"name": "限量商品", "price": 100.0, "stock": 3}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("尝试购买超过库存的数量"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": 10
#             }, headers=auth_headers)
#             assert resp.status_code == 400
#             assert "库存不足" in resp.json()["detail"]
#
#     @allure.story("订单异常")
#     @allure.title("未授权访问——不带 Token 下单应返回 401")
#     def test_order_unauthorized(self, base_url):
#         """不带 Token 访问下单接口，预期返回 401"""
#         with allure.step("不带 Token 发送下单请求"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": 1, "quantity": 1
#             })
#             assert resp.status_code == 401



# # test_negative.py
# import pytest
# import requests
# import time
# import allure
#
# @allure.feature("异常流测试")
# class TestNegativeScenarios:
#
#     # ==================== 用户注册异常 ====================
#
#     @allure.story("注册异常")
#     @allure.title("重复用户名注册应返回 400")
#     def test_register_duplicate_username(self, base_url):
#         """重复注册相同用户名，预期返回 400"""
#         unique_id = int(time.time_ns())
#         username = f"dup_{unique_id}"
#         payload = {"username": username, "password": "123456", "email": f"dup_{unique_id}@test.com"}
#
#         with allure.step("第一次注册"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 200
#
#         with allure.step("第二次注册（重复）"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 400
#             assert "用户名已注册" in resp.json()["detail"]
#
#     @allure.story("注册异常")
#     @allure.title("重复邮箱注册应返回 500（数据库约束）")
#     def test_register_duplicate_email(self, base_url):
#         """重复邮箱触发数据库 UNIQUE 约束，后端应处理"""
#         unique_id = int(time.time_ns())
#         username_a = f"user_a_{unique_id}"
#         username_b = f"user_b_{unique_id}"
#         email = f"dupemail_{unique_id}@test.com"
#
#         with allure.step("第一个用户注册"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_a, "password": "123456", "email": email
#             })
#             assert resp.status_code == 200
#
#         with allure.step("第二个用户使用相同邮箱"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_b, "password": "123456", "email": email
#             })
#             # SQLAlchemy IntegrityError 触发 500 状态码
#             assert resp.status_code == 500
#
#     # ==================== 商品管理异常 ====================
#
#     @allure.story("商品异常")
#     @allure.title("价格为负数应拒绝")
#     def test_product_negative_price(self, base_url, auth_headers):
#         """商品价格不能为负数"""
#         payload = {"name": "负价格商品", "price": -999.0, "stock": 10}
#         with allure.step("发送负数价格请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             # FastAPI 默认不校验价格范围，需要后端代码做业务校验
#             # 如果需要严格校验，应在 main.py 的 ProductCreate 或 create_product 中添加逻辑
#             assert resp.status_code in [400, 422]
#
#     @allure.story("商品异常")
#     @allure.title("库存为负数应拒绝")
#     def test_product_negative_stock(self, base_url, auth_headers):
#         """商品库存不能为负数"""
#         payload = {"name": "负库存商品", "price": 100.0, "stock": -1}
#         with allure.step("发送负数库存请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             assert resp.status_code in [400, 422]
#
#     # ==================== 订单管理异常 ====================
#
#     @allure.story("订单异常")
#     @allure.title("购买数量为负数应拒绝")
#     def test_order_negative_quantity(self, base_url, auth_headers):
#         """下单数量不能为负数"""
#         product_payload = {"name": "正常商品", "price": 50.0, "stock": 10}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("发送负数数量下单"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": -1
#             }, headers=auth_headers)
#             assert resp.status_code in [400, 422]
#
#     @allure.story("订单异常")
#     @allure.title("超卖场景——库存不足应返回 400")
#     def test_order_oversell(self, base_url, auth_headers):
#         """购买数量大于库存，预期返回 400"""
#         product_payload = {"name": "限量商品", "price": 100.0, "stock": 3}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("尝试购买超过库存的数量"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": 10
#             }, headers=auth_headers)
#             assert resp.status_code == 400
#             assert "库存不足" in resp.json()["detail"]
#
#     @allure.story("订单异常")
#     @allure.title("未授权访问——不带 Token 下单应返回 401")
#     def test_order_unauthorized(self, base_url):
#         """不带 Token 访问下单接口，预期返回 401"""
#         with allure.step("不带 Token 发送下单请求"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": 1, "quantity": 1
#             })
#             assert resp.status_code == 401



# # test_negative.py
# import pytest
# import requests
# import time
# import allure
#
# @allure.feature("异常流测试")
# class TestNegativeScenarios:
#
#     # ==================== 用户注册异常 ====================
#
#     @allure.story("注册异常")
#     @allure.title("重复用户名注册应返回 400")
#     def test_register_duplicate_username(self, base_url):
#         """重复注册相同用户名，预期返回 400"""
#         unique_id = int(time.time_ns())
#         username = f"dup_{unique_id}"
#         payload = {"username": username, "password": "123456", "email": f"dup_{unique_id}@test.com"}
#
#         with allure.step("第一次注册"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 200
#
#         with allure.step("第二次注册（重复）"):
#             resp = requests.post(f"{base_url}/register", json=payload)
#             assert resp.status_code == 400
#             assert "用户名已注册" in resp.json()["detail"]
#
#     @allure.story("注册异常")
#     @allure.title("重复邮箱注册应返回 400")
#     def test_register_duplicate_email(self, base_url):
#         """重复邮箱触发业务校验，预期返回 400"""
#         unique_id = int(time.time_ns())
#         username_a = f"user_a_{unique_id}"
#         username_b = f"user_b_{unique_id}"
#         email = f"dupemail_{unique_id}@test.com"
#
#         with allure.step("第一个用户注册"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_a, "password": "123456", "email": email
#             })
#             assert resp.status_code == 200
#
#         with allure.step("第二个用户使用相同邮箱"):
#             resp = requests.post(f"{base_url}/register", json={
#                 "username": username_b, "password": "123456", "email": email
#             })
#             # 后端逻辑优先检查用户名，邮箱重复通常也返回 400 或 500。
#             # 由于我们也没对邮箱做唯一约束，这里只校验非 200 即可。
#             assert resp.status_code != 200
#
#     # ==================== 商品管理异常 ====================
#
#     @allure.story("商品异常")
#     @allure.title("价格为负数应拒绝(422)")
#     def test_product_negative_price(self, base_url, auth_headers):
#         """商品价格不能为负数"""
#         payload = {"name": "负价格商品", "price": -999.0, "stock": 10}
#         with allure.step("发送负数价格请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             # Pydantic Field 校验失败会返回 422
#             assert resp.status_code == 422
#
#     @allure.story("商品异常")
#     @allure.title("库存为负数应拒绝(422)")
#     def test_product_negative_stock(self, base_url, auth_headers):
#         """商品库存不能为负数"""
#         payload = {"name": "负库存商品", "price": 100.0, "stock": -1}
#         with allure.step("发送负数库存请求"):
#             resp = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             assert resp.status_code == 422
#
#     # ==================== 订单管理异常 ====================
#
#     @allure.story("订单异常")
#     @allure.title("购买数量为负数应拒绝(422)")
#     def test_order_negative_quantity(self, base_url, auth_headers):
#         """下单数量不能为负数"""
#         product_payload = {"name": "正常商品", "price": 50.0, "stock": 10}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("发送负数数量下单"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": -1
#             }, headers=auth_headers)
#             assert resp.status_code == 422
#
#     @allure.story("订单异常")
#     @allure.title("超卖场景——库存不足应返回 400")
#     def test_order_oversell(self, base_url, auth_headers):
#         """购买数量大于库存，预期返回 400"""
#         product_payload = {"name": "限量商品", "price": 100.0, "stock": 3}
#         resp = requests.post(f"{base_url}/products", json=product_payload, headers=auth_headers)
#         assert resp.status_code == 200
#         product_id = resp.json()["id"]
#
#         with allure.step("尝试购买超过库存的数量"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": product_id, "quantity": 10
#             }, headers=auth_headers)
#             assert resp.status_code == 400
#             assert "库存不足" in resp.json()["detail"]
#
#     @allure.story("订单异常")
#     @allure.title("未授权访问——不带 Token 下单应返回 401")
#     def test_order_unauthorized(self, base_url):
#         """不带 Token 访问下单接口，预期返回 401"""
#         with allure.step("不带 Token 发送下单请求"):
#             resp = requests.post(f"{base_url}/orders", json={
#                 "product_id": 1, "quantity": 1
#             })
#             assert resp.status_code == 401
