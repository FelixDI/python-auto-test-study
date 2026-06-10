#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 14:49
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : product_api.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 商品管理


from src.ecommerce_api_test.common.base_api import BaseApi


class ProductApi(BaseApi):
    def create_product(self, name: str, price: float, stock: int):
        data = {
            "name": name,
            "price": price,
            "stock": stock
        }
        return self.post(endpoint="/products", json=data)

    # main.py中定义了URL参数 Requests模块提供了params自动拼接URL 后面的查询参数 /products?skip=0&limit=100
    # skip跳过多少条 limit每页最多返回多少条  skip=0, limit=100 ：默认从第一条开始，最多返回100条数据
    def list_products(self, skip: int = 0, limit: int = 100):
        params = {"skip": skip, "limit": limit}
        return self.get(endpoint="/products", params=params)

    def get_product(self, product_id: int):
        return self.get(f"/products/{product_id}")

    # def delete_product(self, product_id: int):
    #     return self.delete(f"/products/{product_id}")