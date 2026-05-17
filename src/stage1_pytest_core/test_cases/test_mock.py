#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-16 21:01
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_mock.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : mock模拟任何外部依赖的测试环境 让测试快速、稳定、隔离

import pytest
from unittest.mock import Mock,MagicMock,patch
import requests

def test_mock_basic():
    fake_api = Mock()
    fake_api.get_user.return_value = {"name":"张三", "age":25}

    result = fake_api.get_user(123)
    assert result["name"] == "张三"
    assert result["age"] == 25

    fake_api.get_user.assert_called_once_with(123)


def test_mock_side_effect():
    fake_db = Mock()

    fake_db.next_id.side_effect = [1, 2, RuntimeError("连接断开")]
    assert fake_db.next_id() == 1
    assert fake_db.next_id() == 2
    with pytest.raises(RuntimeError, match="连接断开"):
        fake_db.next_id()


def test_magic_mock():
    fake_dict = MagicMock()
    fake_dict.__getitem__.return_value = "mocked_value"
    fake_dict.__len__.return_value = 3

    assert fake_dict["any_key"] == "mocked_value"
    assert len(fake_dict) == 3

# 如果是【函数内部导入】→ 写 @patch("原始模块名.函数名")
#     ↓
# 如果是【模块顶部导入】→ 写 @patch("被测试代码所在的模块名.变量名")
#     ↓
#     → 如果导入方式是 import time → 变量名是 time.sleep
#     → 如果导入方式是 from time import sleep → 变量名是 sleep    不建议 容易混乱

# 采用完整路径调用能规避很多调用错误
# @patch("requests.get")  # 简写不推荐 容易和函数内部导入的情况混淆
@patch("test_mock.requests.get")
def test_patch_requests_get(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status":"ok"}
    mock_get.return_value = mock_response

    response = requests.get("http://api.example.com/data")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

    mock_get.assert_called_once()


def test_patch_context():
    with patch("builtins.open") as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "fake content"

        with open("不存在的文件.txt") as f:
            content = f.read()
            assert content == "fake content"


def send_notification(user_id):
    from time import sleep
    # import time        不管哪种导入形式 因为是函数内导入 均采用   @patch("原始模块名.函数名")
    # time.sleep(0.1)
    sleep(0.1)
    return f"通知已发送给客户{user_id}"

def test_send_notification():
    result = send_notification(123)
    assert "123" in result

@patch("time.sleep")
def test_send_notification_mocked(mock_sleep):

    result = send_notification(123)
    assert "123" in result
    mock_sleep.assert_called_once()


### test_mock.py
# import pytest
# from unittest.mock import Mock, MagicMock, patch
# import requests
#
# # ==================== 1. Mock 基本用法 ====================
# def test_mock_basic():
#     """模拟一个对象，指定返回值"""
#     fake_api = Mock()
#     fake_api.get_user.return_value = {"name": "张三", "age": 25}
#
#     # 调用 fake 替代真实 API
#     result = fake_api.get_user(123)
#     assert result["name"] == "张三"
#     assert result["age"] == 25
#
#     # 验证被调用过
#     fake_api.get_user.assert_called_once_with(123)
#
# # ==================== 2. side_effect：模拟异常或多次调用 ====================
# def test_mock_side_effect():
#     """模拟依次返回不同值，最后一次抛异常"""
#     fake_db = Mock()
#     # 第一次调用返回 1，第二次返回 2，第三次抛异常
#     fake_db.next_id.side_effect = [1, 2, RuntimeError("连接断开")]
#
#     assert fake_db.next_id() == 1
#     assert fake_db.next_id() == 2
#     with pytest.raises(RuntimeError, match="连接断开"):
#         fake_db.next_id()
#
# # ==================== 3. MagicMock：自动模拟魔术方法 ====================
# def test_magic_mock():
#     """MagicMock 支持 __len__、__getitem__ 等"""
#     fake_dict = MagicMock()
#     fake_dict.__getitem__.return_value = "mocked_value"
#     fake_dict.__len__.return_value = 3
#
#     assert fake_dict["any_key"] == "mocked_value"
#     assert len(fake_dict) == 3
#
# # ==================== 4. patch 装饰器：替换真实模块 ====================
# @patch("requests.get")
# def test_patch_requests_get(mock_get):
#     """用 patch 拦截 requests.get，不真发请求"""
#     # 构造假的响应对象
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"status": "ok"}
#     mock_get.return_value = mock_response
#
#     # 被测代码：里面调了 requests.get
#     response = requests.get("http://api.example.com/data")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}
#
#     # 验证确实被调用了一次
#     mock_get.assert_called_once()
#
# # ==================== 5. patch 上下文管理器 ====================
# def test_patch_context():
#     """只在 with 块内生效的 mock"""
#     with patch("builtins.open") as mock_open:
#         mock_open.return_value.__enter__.return_value.read.return_value = "fake content"
#
#         with open("不存在的文件.txt") as f:
#             content = f.read()
#             assert content == "fake content"
#
# # ==================== 6. 模拟被测函数内部的依赖 ====================
# def send_notification(user_id):
#     """被测函数：内部调用了外部邮件服务"""
#     from time import sleep
#     sleep(0.1)  # 模拟耗时
#     return f"通知已发送给用户 {user_id}"
#
# def test_send_notification():
#     """不需要 mock，直接测就行（这是纯逻辑函数）"""
#     result = send_notification(123)
#     assert "123" in result
#
# @patch("time.sleep")  # 替换 time.sleep，避免真等
# def test_send_notification_mocked(mock_sleep):
#     """用 mock 替换 sleep，测试瞬间完成"""
#     result = send_notification(123)
#     assert "123" in result
#     mock_sleep.assert_called_once()



