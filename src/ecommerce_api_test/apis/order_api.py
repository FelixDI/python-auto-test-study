#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 15:34
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : order_api.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 订单管理


from src.ecommerce_api_test.common.base_api import BaseApi


class OrderApi(BaseApi):
    def create_order(self, product_id: int, quantity: int):
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        return self.post("/orders", json=data)

    def get_order(self, order_id: int):
        return self.get(f"/orders/{order_id}")