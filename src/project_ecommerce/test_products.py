#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-26 17:09
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_products.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 商品管理测试


import pytest
import requests
import allure

@allure.feature("商品管理")
class TestProducts:

    @allure.story("添加商品")
    @allure.title("管理员添加新商品")
    def test_add_product(self,base_url,auth_headers):
        payload = {"name":"测试商品","price":99.9,"stock":10}
        with allure.step("发送添加商品请求"):
            response = requests.post(f"{base_url}/products",json=payload,headers=auth_headers)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == payload["name"]
            assert data["price"] == payload["price"]
            assert data["stock"] == payload["stock"]

# main.py，查询商品列表和获取单个商品接口并没有要求鉴权（只是 POST 商品需要鉴权） 不需要传 auth_headers

    @allure.story("查询商品")
    @allure.title("查询所有商品")
    def test_list_products(self,base_url):
        with allure.step("获取商品列表"):
            response = requests.get(f"{base_url}/products")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data,list)

    @allure.story("查询商品")
    @allure.title("查询不存在的商品应返回404")
    def test_get_product_not_found(self,base_url):
        with allure.step("查询不存在商品"):
            response = requests.get(f"{base_url}/products/99999")
            assert response.status_code == 404


# # test_products.py
# import pytest
# import requests
# import allure
#
# @allure.feature("商品管理")
# class TestProducts:
#
#     @allure.story("添加商品")
#     @allure.title("管理员添加新商品")
#     def test_add_product(self, base_url, auth_headers):
#         payload = {"name": "测试商品", "price": 99.9, "stock": 10}
#         with allure.step("发送添加商品请求"):
#             response = requests.post(f"{base_url}/products", json=payload, headers=auth_headers)
#             assert response.status_code == 200
#             data = response.json()
#             assert data["name"] == payload["name"]
#             assert data["price"] == payload["price"]
#             assert data["stock"] == payload["stock"]
#
#     @allure.story("查询商品")
#     @allure.title("查询所有商品")
#     def test_list_products(self, base_url):
#         with allure.step("获取商品列表"):
#             response = requests.get(f"{base_url}/products")
#             assert response.status_code == 200
#             data = response.json()
#             assert isinstance(data, list)
#
#     @allure.story("查询商品")
#     @allure.title("查询不存在的商品应返回404")
#     def test_get_product_not_found(self, base_url):
#         with allure.step("查询不存在商品"):
#             response = requests.get(f"{base_url}/products/99999")
#             assert response.status_code == 404