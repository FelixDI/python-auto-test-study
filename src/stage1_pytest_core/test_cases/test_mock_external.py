#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-17 18:13
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_mock_external.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : more mock


import pytest
from unittest.mock import Mock,patch

class EmailService:
    def send(self,to,subject,body):
        # to：收件邮箱
        # subject：邮件标题
        # body：邮件正文内容

        return f"邮件已发送给{to}"

class UserManager:
    def __init__(self,email_service):
        self.email_service = email_service

    def register(self,username,email):
        message = self.email_service.send(email,"欢迎注册",f"你好{username}")
        return {"code":200,"msg":message}

def test_register_without_mock():
    real_email = EmailService()
    manager = UserManager(real_email)
    result = manager.register("test_user", "test@example.com")
    assert result["code"] == 200

def test_register_with_mock():
    mock_email = Mock()   # 创建一个空的、万能的假对象
    mock_email.send.return_value = "Mock邮件已发送给test@example.com"
    #Mock 对象本身没有任何方法。你写什么方法，它就 “变” 出什么方法xxx.return_value = 结果->造假返回值，用于测试，不运行真实代码

    manager = UserManager(mock_email)
    result = manager.register("test_user", "test@example.com")
    assert result["code"] == 200
    assert "Mock邮件" in result["msg"]

    mock_email.send.assert_called_once_with("test@example.com","欢迎注册","你好test_user")
#assert_called_once_with()	查 调用 1 次 + 参数正确	必须传参

def fetch_user_info(user_id):
    import requests
    response = requests.get(f"http://api.example.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()

    return None

@patch("requests.get")
def test_fetch_user_info_mocked(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id":1, "name":"张三"}
    mock_get.return_value = mock_response

    result = fetch_user_info(1)

    assert result["name"] == "张三"
    mock_get.assert_called_once()   # 只查调用了 1 次	，不能传参


## test_mock_external.py
# import pytest
# from unittest.mock import Mock, patch
#
# # ==================== 模拟外部邮件服务 ====================
# class EmailService:
#     """真实邮件服务（被测对象依赖它）"""
#     def send(self, to, subject, body):
#         # 真实发邮件，测试时不能真发
#         return f"邮件已发送给 {to}"
#
# class UserManager:
#     """被测对象：用户管理器"""
#     def __init__(self, email_service):
#         self.email_service = email_service
#
#     def register(self, username, email):
#         # 注册后发欢迎邮件
#         message = self.email_service.send(email, "欢迎注册", f"你好 {username}")
#         return {"code": 200, "msg": message}
#
# # 不用 Mock：真发邮件（测试不应该这样写）
# def test_register_without_mock():
#     real_email = EmailService()
#     manager = UserManager(real_email)
#     result = manager.register("test_user", "test@example.com")
#     assert result["code"] == 200
#
# # 用 Mock：不发真邮件
# def test_register_with_mock():
#     # 创建假的邮件服务
#     mock_email = Mock()
#     mock_email.send.return_value = "Mock 邮件已发送给 test@example.com"
#
#     # 注入假服务
#     manager = UserManager(mock_email)
#     result = manager.register("test_user", "test@example.com")
#
#     # 断言
#     assert result["code"] == 200
#     assert "Mock 邮件" in result["msg"]
#
#     # 验证 send 被正确调用
#     mock_email.send.assert_called_once_with(
#         "test@example.com", "欢迎注册", "你好 test_user"
#     )
#
# # ==================== patch 方式 Mock requests ====================
# def fetch_user_info(user_id):
#     """被测函数：调用外部 API 获取用户信息"""
#     import requests
#     response = requests.get(f"http://api.example.com/users/{user_id}")
#     if response.status_code == 200:
#         return response.json()
#     return None
#
# @patch("test_mock_external.requests.get")
# def test_fetch_user_info_mocked(mock_get):
#     """使用 patch 装饰器 Mock requests.get"""
#     # 构造假响应
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"id": 1, "name": "张三"}
#     mock_get.return_value = mock_response
#
#     result = fetch_user_info(1)
#
#     assert result["name"] == "张三"
#     mock_get.assert_called_once()


