#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-10 09:26
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : base_api.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 采用 API Object Pattern 设计模式重构电商接口自动化测试项目, API test review


import requests
import json
import time
import pytest

from typing import Dict, Any, Optional


class BaseApi:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()  # 所有请求共用一个Session
        # 默认请求头
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent":"Ecommerce-Api-Test/1.0"
        })
        self.response = None
        self.response_time = None
        self.token: Optional[str] = None

    def set_auth_token(self, token: str):
        self.token = token  # 注入JWT Token
        self.session.headers["Authorization"] = f"Bearer {token}"  # Authorization: Bearer xxxxx

    def clear_auth_token(self):
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    # 封装_request()一方面少写代码，且方便后续统一添加logging日志、重试、超时、Allure等公共逻辑；大项目价值很大
    # allure更多放在测试层比较妥当
    # def _request(self, method, path, **kwargs):
    #     # 默认超时
    #     kwargs.setdefault("timeout", 10)
    #
    #     # 日志
    #     logger.info(...)
    #
    #     start = time.time()
    #
    #     #重试
    #     try:
    #
    #         resp = self.session.request(
    #             method,
    #             f"{self.base_url}{path}",
    #             **kwargs
    #         )
    #
    #     except Exception:
    #         logger.exception("请求失败")
    #         raise
    #     # 响应时间统计
    #     elapsed = time.time() - start
    #
    #     logger.info(
    #         f"状态码:{resp.status_code}"
    #     )
    #
    #     logger.info(
    #         f"耗时:{elapsed:.3f}s"
    #     )
    #
    #     return resp
    # **kwargs 不提前规定参数，把所有额外参数打包转发
    # (可变位置参数*args 收集多余的位置参数到元组，可变关键字参数**kwargs 收集多余的关键字参数到字典)
    # json、data、files、cookies、timeout、verify、proxies

    # requests.get(url) 本质上就是Requests 官方对 requests.request("GET", url)的封装
    # def get(url, **kwargs):
    #     return request(
    #         "GET",
    #         url,
    #         **kwargs
    #     )
    # 模仿框架设计代码,ecommerce实战项目代码进行封装的实践_request
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        start_time = time.time()
        url = f"{self.base_url}{endpoint}"
        self.response = self.session.request(method=method, url=url, **kwargs)
        self.response_time = time.time() - start_time
        return self.response

    # 封装HTTP常用方法
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request(method="GET", endpoint=endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request(method="POST", endpoint=endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request(method="PUT", endpoint=endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request(method="DELETE", endpoint=endpoint, **kwargs)

    # def get_json(self):
    #     try:
    #         return self.response.json()
    #     except json.JSONDecodeError:
    #         pytest.fail("响应不是有效的JSON格式")

    def assert_status_code(self, expected_status: int):
        assert self.response.status_code == expected_status, \
        f"状态码错误：预期{expected_status}，实际{self.response.status_code}"

    def assert_json_data(self, expected_data: Dict[str, Any]):
        # actual_data = self.get_json()

        try:
            actual_data = self.response.json()
        except json.JSONDecodeError:
            pytest.fail("响应不是有效的JSON格式")

        for key, value in expected_data.items():
            assert key in actual_data, f"响应缺少字段：{key}"
            assert actual_data[key] == value, \
            f"字段值{key}错误：预期{value}，实际{actual_data[key]}"

    def assert_response_time_less_than(self, max_seconds: float):
        assert self.response_time < max_seconds, \
        f"响应超时：{self.response_time:.2f}秒>{max_seconds}秒"

    def assert_json_has_fields(self, fields: list):
        try:
            actual_data = self.response.json()
        except json.JSONDecodeError:
            pytest.fail("响应不是有效的JSON格式")

        for field in fields:
            assert field in actual_data, f"响应缺少必填字段：{field}"

    def assert_error_message(self, expected_message: str):
        try:
            actual_data = self.response.json()
        except json.JSONDecodeError:
            pytest.fail("响应不是有效的JSON格式")

        assert "detail" in actual_data, "错误响应缺少detail字段"
        assert expected_message in actual_data["detail"], \
        f"错误信息不匹配：预期包含'{expected_message}'，实际是'{actual_data['detail']}'"

    def close(self) -> None:
        self.session.close()


# # src/ecommerce_api_test/common/base_api.py
# import requests
# from typing import Dict, Any, Optional
# import json
# import time
#
# class BaseApi:
#     """所有接口的基类，封装通用HTTP方法和JWT认证"""
#
#     def __init__(self, base_url: str = "http://localhost:8000"):
#         self.base_url = base_url
#         self.session = requests.Session()
#         self.session.headers.update({
#             "Content-Type": "application/json",
#             "User-Agent": "Ecommerce-Api-Test/1.0"
#         })
#         self.response = None
#         self.response_time = None
#         self.token = None
#
#     def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
#         """发送GET请求"""
#         url = f"{self.base_url}{endpoint}"
#         start_time = time.time()
#         self.response = self.session.get(url, params=params, **kwargs)
#         self.response_time = time.time() - start_time
#         return self.response
#
#     def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
#         """发送POST请求"""
#         url = f"{self.base_url}{endpoint}"
#         start_time = time.time()
#         self.response = self.session.post(url, json=json, **kwargs)
#         self.response_time = time.time() - start_time
#         return self.response
#
    # def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
    #     """发送PUT请求"""
    #     url = f"{self.base_url}{endpoint}"
    #     start_time = time.time()
    #     self.response = self.session.put(url, json=json, **kwargs)
    #     self.response_time = time.time() - start_time
    #     return self.response
    #
    # def delete(self, endpoint: str, **kwargs) -> requests.Response:
    #     """发送DELETE请求"""
    #     url = f"{self.base_url}{endpoint}"
    #     start_time = time.time()
    #     self.response = self.session.delete(url, **kwargs)
    #     self.response_time = time.time() - start_time
    #     return self.response

#     def set_auth_token(self, token: str):
#         """设置JWT认证Token，后续所有请求自动携带"""
#         self.token = token
#         self.session.headers["Authorization"] = f"Bearer {token}"
#
#     def clear_auth_token(self):
#         """清除认证Token"""
#         self.token = None
#         if "Authorization" in self.session.headers:
#             del self.session.headers["Authorization"]
#
#     def assert_status_code(self, expected_status: int):
#         """断言响应状态码"""
#         assert self.response.status_code == expected_status, \
#             f"状态码错误：预期{expected_status}，实际{self.response.status_code}"
#
#     def assert_json_contains(self, expected_data: Dict[str, Any]):
#         """断言JSON响应包含指定字段和值"""
#         try:
#             actual_data = self.response.json()
#         except json.JSONDecodeError:
#             pytest.fail("响应不是有效的JSON格式")
#
#         for key, value in expected_data.items():
#             assert key in actual_data, f"响应缺少字段：{key}"
#             assert actual_data[key] == value, \
#                 f"字段{key}值错误：预期{value}，实际{actual_data[key]}"
#
#     def assert_response_time_less_than(self, max_seconds: float):
#         """断言响应时间小于指定值"""
#         assert self.response_time < max_seconds, \
#             f"响应超时：{self.response_time:.2f}秒 > {max_seconds}秒"
#
#     def assert_json_has_fields(self, fields: list):
#         """断言JSON响应包含所有指定字段"""
#         try:
#             actual_data = self.response.json()
#         except json.JSONDecodeError:
#             pytest.fail("响应不是有效的JSON格式")
#
#         for field in fields:
#             assert field in actual_data, f"响应缺少必填字段：{field}"
#
#     def assert_error_message(self, expected_message: str):
#         """断言错误响应包含指定信息"""
#         try:
#             actual_data = self.response.json()
#         except json.JSONDecodeError:
#             pytest.fail("响应不是有效的JSON格式")
#
#         assert "detail" in actual_data, "错误响应缺少detail字段"
#         assert expected_message in actual_data["detail"], \
#             f"错误信息不匹配：预期包含'{expected_message}'，实际是'{actual_data['detail']}'"
#
#     def close(self):
#         """关闭会话"""
#         self.session.close()