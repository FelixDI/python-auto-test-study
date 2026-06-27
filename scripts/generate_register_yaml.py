#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-27 10:59
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : generate_register_yaml.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 造测试用例  YAML可读性好，支持注释、层级结构，测试人员容易维护 ；yaml作配置文件 也是Python 测试生态的主流


import yaml
from faker import Faker

fake = Faker("zh_CN")

def generate_normal_cases(count=20):
    """生成正向用例数据"""
    cases = []
    for _ in range(count):
        cases.append({
            "username": fake.unique.user_name(),
            "phone": fake.unique.phone_number(),
            "password": "Test@1234",
            "expect_code": 200,
            "expect_msg": "注册成功"
        })
    return cases

def generate_error_cases():
    """手动构造异常边界用例（Faker 生成不了，必须手动设计）"""
    return [
        {
            "username": "",
            "phone": "13800138000",
            "password": "Test@1234",
            "expect_code": 400,
            "expect_msg": "用户名不能为空"
        },
        {
            "username": "test001",
            "phone": "1380013800",  # 10位手机号
            "password": "Test@1234",
            "expect_code": 400,
            "expect_msg": "手机号格式错误"
        },
        {
            "username": "test002",
            "phone": "13800138000",
            "password": "123",  # 密码过短
            "expect_code": 400,
            "expect_msg": "密码长度不能小于6位"
        }
    ]

if __name__ == "__main__":
    test_data = {
        "normal_cases": generate_normal_cases(20),
        "error_cases": generate_error_cases()
    }

    # 写入 YAML 文件
    with open("data/register_cases.yaml", "w", encoding="utf-8") as f:
        yaml.dump(test_data, f, allow_unicode=True, sort_keys=False)

    print("注册接口测试数据已生成，保存到 data/register_cases.yaml")