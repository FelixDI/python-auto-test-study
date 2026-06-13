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

    # # 未实现的功能
    # def get_orders(self):
    #     return self.get("/orders")

    # # 订单购买一种或多种商品 统一方法 items=[{}]   items=[{},{},{}...]
    # def create_order_multiple_items(self, items: list[dict]):
    #     payload = {"items": items}
    #     return self.post("/orders", json=payload)
    #
    # # 很多业务对象（订单、用户、商品）并不会真正执行 DELETE SQL，而是通过状态流转或软删除保留历史数据，保证审计、对账和业务追溯能力。
    # def cancel_order(self, order_id: int):
    #     return self.post(f"/orders/{order_id}/cancel")