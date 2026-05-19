#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-19 16:47
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_mock_external.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : review mock

# 真实项目中：被测服务调了支付接口 → Mock 掉，不真扣钱
# 被测服务调了短信接口 → Mock 掉，不真发短信
# 被测服务调了第三方天气 API → Mock 掉，返回可控


import pytest
from unittest.mock import Mock,patch
import requests

class TestMockExternal:

    def test_mock_external_api_with_object(self):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value ={
            "city":"北京",
            "temperature":25,
            "weather":"晴"
        }

        def get_weather(city):
            return mock_response

        response = get_weather("北京")
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "北京"
        assert data["temperature"] == 25
        assert isinstance(data["temperature"], int)
        assert data["weather"] == "晴"

# import顶部导入 patch写完整调用路径 不简写  函数内导入写 源模块路径   不易混淆
    @patch("test_mock_external.requests.get")
    # @patch("requests.get")
    def test_mock_external_api_with_patch(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"city":"上海","temperature":30}

        mock_get.return_value = mock_response    #   get_weather()

        def fetch_weather(city):
            response = requests.get(f"http://api.weather.com/{city}")
            if response.status_code == 200:
                return response.json()
            return None

        result = fetch_weather("上海")
        assert result["city"] == "上海"
        assert result["temperature"] == 30
        mock_get.assert_called_once()



# 测试超时异常	模拟 requests.get() 直接抛出 Timeout 异常
    # 只需设置 mock_get.side_effect = requests.exceptions.Timeout(...)，不需要任何响应对象 Mock()
    @patch("test_mock_external.requests.get")
    def test_mock_external_api_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("连接超时")

        def fetch_weather(city):
            try:
                response = requests.get(f"http://api.weather.com/{city}", timeout=5)
                return response.json()
            except requests.exceptions.Timeout:
                return {"error":"请求超时"}

        result = fetch_weather("深圳")
        assert result["error"] == "请求超时"
        mock_get.assert_called_once()


    @patch("test_mock_external.requests.get")
    def test_mock_external_api_500(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        def fetch_weather(city):
            response = requests.get(f"http://api.weather.com/{city}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error":f"外部服务异常:{response.status_code}"}

        result = fetch_weather("广州")
        assert result["error"] == "外部服务异常:500"
        mock_get.assert_called_once()


# # test_mock_external.py
# import requests
# import pytest
# from unittest.mock import Mock, patch
#
#
# # ==================== 场景：模拟外部 API 调用 ====================
#
# class TestMockExternal:
#     """
#     假设被测服务内部有一个函数，会调用外部天气 API 来获取天气信息。
#     我们不希望测试时真的去请求外部 API，所以用 Mock 替换它。
#     """
#
#     # ---------- 方式一：用 Mock 对象 ----------
#     def test_mock_external_api_with_object(self):
#         """
#         模拟外部 API 调用：创建一个假的响应对象，替换真实请求
#         """
#         # 1. 创建一个假的 response 对象
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             "city": "北京",
#             "temperature": 25,
#             "weather": "晴"
#         }
#
#         # 2. 模拟被测函数（实际项目中这个函数在别的模块里）
#         def get_weather(city):
#             """被测函数：内部会调用外部 API"""
#             # 真实代码：response = requests.get(f"http://api.weather.com/{city}")
#             # 测试时用 mock_response 替代
#             return mock_response
#
#         # 3. 调用被测函数并断言
#         response = get_weather("北京")
#         assert response.status_code == 200
#
#         data = response.json()
#         assert data["city"] == "北京"
#         assert data["temperature"] == 25
#         assert isinstance(data["temperature"], int)
#         assert data["weather"] == "晴"
#
#     # ---------- 方式二：用 patch 替换 requests.get ----------
#     @patch("requests.get")
#     def test_mock_external_api_with_patch(self, mock_get):
#         """
#         用 patch 直接替换 requests.get 的返回值
#         这样被测函数内部调用 requests.get 时拿到的就是假响应
#         """
#         # 1. 构造假响应
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {"city": "上海", "temperature": 30}
#
#         # 2. 设置 mock_get 的返回值
#         mock_get.return_value = mock_response
#
#         # 3. 调用被测函数（内部会调用 requests.get）
#         def fetch_weather(city):
#             """模拟真实的业务函数"""
#             response = requests.get(f"http://api.weather.com/{city}")
#             if response.status_code == 200:
#                 return response.json()
#             return None
#
#         result = fetch_weather("上海")
#
#         # 4. 断言返回值
#         assert result["city"] == "上海"
#         assert result["temperature"] == 30
#
#         # 5. 验证 requests.get 确实被调用了
#         mock_get.assert_called_once()
#
#     # ---------- 方式三：模拟异常 ----------
#     @patch("requests.get")
#     def test_mock_external_api_timeout(self, mock_get):
#         """
#         模拟外部 API 调用超时，验证被测函数的异常处理逻辑
#         """
#         # 设置 side_effect 让 requests.get 抛出超时异常
#         mock_get.side_effect = requests.exceptions.Timeout("连接超时")
#
#         def fetch_weather(city):
#             """被测函数：带异常处理的版本"""
#             try:
#                 response = requests.get(f"http://api.weather.com/{city}", timeout=5)
#                 return response.json()
#             except requests.exceptions.Timeout:
#                 return {"error": "请求超时"}
#
#         result = fetch_weather("深圳")
#
#         # 断言异常处理后的默认返回值
#         assert result == {"error": "请求超时"}
#         mock_get.assert_called_once()
#
#     # ---------- 方式四：模拟接口返回错误状态码 ----------
#     @patch("requests.get")
#     def test_mock_external_api_500(self, mock_get):
#         """
#         模拟外部 API 返回 500 错误，验证被测函数如何处理
#         """
#         mock_response = Mock()
#         mock_response.status_code = 500
#         mock_response.text = "Internal Server Error"
#         mock_get.return_value = mock_response
#
#         def fetch_weather(city):
#             response = requests.get(f"http://api.weather.com/{city}")
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 return {"error": f"外部服务异常: {response.status_code}"}
#
#         result = fetch_weather("广州")
#
#         assert result["error"] == "外部服务异常: 500"
#         mock_get.assert_called_once()
