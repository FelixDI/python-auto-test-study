#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-13 11:26
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : combine123_testdataprocess.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 前三块的知识点汇总综合练习1 测试数据处理脚本

test_cases = [
    {
        'id': 'TC001',
        'desc': '正常登录',
        'url':'/api/v1/login',
        'method': 'POST',
        'body': {
            'username': 'admin',
            'password': '123456'
        },
        'excepted_code': 200
    },
    {
        'id': 'TC002',
        'desc': '缺少密码',
        'url': '/api/v1/login',
        'method': 'POST',
        'body': {'username': 'admin'},
        'excepted_code': 400
    },
    {
        'id': 'TC003',
        'desc': '获取用户信息',
        'url': '/api/v1/users/10086',
        'method': 'GET',
        'body': None,
        'excepted_code': 200
    },
]


def fake_request(method, url, body=None):
    if body and 'password' in body:
        return 200
    elif body and 'password' not in body:
        return 400
    return 200

results = []

for case in test_cases:
    print(f'执行{case['id']}: {case['desc']}')

    if case["body"]:
        print(f" 请求: {case['method']} {case['url']} body={case['body']}")
    else:
        print(f" 请求: {case['method']}{case['url']}")

    actual_code = fake_request(case['method'], case['url'], case['body'])

    passed = actual_code == case['excepted_code']
    status = "PASS"if passed else "FAIL"
    print(f" 期望: {case['excepted_code']}, 实际: {actual_code} -> {status}")

    results.append({
        "id": case["id"],
        "desc": case["desc"],
        "status": status
    })
    print()

print("====测试汇总====")
for r in results:
    print(f"{r['id']}{r['desc']}:{r['status']}")


passed_count = sum(1 for r in results if r ['status'] == 'PASS')
total_count = len(results)
print(f"\n通过率: {passed_count}/{total_count} = {passed_count / total_count*100:.1f}%")

# # ============================================
# # 综合练习1：用列表存储测试用例，用字典存储接口请求参数
# # 模拟测试执行：遍历用例 -> 拼装请求 -> 校验预期状态码
# # ============================================
#
# # ------ 定义测试用例（列表 + 字典） ------
# test_cases = [
#     {
#         "id": "TC001",
#         "desc": "正常登录",
#         "url": "/api/v1/login",
#         "method": "POST",
#         "body": {"username": "admin", "password": "123456"},
#         "expected_code": 200,
#     },
#     {
#         "id": "TC002",
#         "desc": "缺少密码",
#         "url": "/api/v1/login",
#         "method": "POST",
#         "body": {"username": "admin"},
#         "expected_code": 400,
#     },
#     {
#         "id": "TC003",
#         "desc": "获取用户信息",
#         "url": "/api/v1/user/10086",
#         "method": "GET",
#         "body": None,                   # GET 无请求体
#         "expected_code": 200,
#     },
# ]
#
# # ------ 模拟执行测试（不真正发请求，用占位函数代替） ------
# def fake_request(method, url, body=None):
#     """模拟接口调用，仅返回固定状态码用于演示"""
#     if body and "password" in body:
#         return 200
#     elif body and "password" not in body:
#         return 400
#     return 200
#
# # ------ 遍历执行并断言 ------
# results = []  # 收集执行结果
#
# for case in test_cases:
#     print(f"执行 {case['id']}: {case['desc']}")
#
#     # 拼装请求打印
#     if case["body"]:
#         print(f"  请求: {case['method']} {case['url']} body={case['body']}")
#     else:
#         print(f"  请求: {case['method']} {case['url']}")
#
#     # 调用模拟接口
#     actual_code = fake_request(case["method"], case["url"], case["body"])
#
#     # 断言
#     passed = actual_code == case["expected_code"]
#     status = "PASS" if passed else "FAIL"
#     print(f"  期望: {case['expected_code']}, 实际: {actual_code} -> {status}")
#
#     # 记录结果（字典存储结果信息）
#     results.append({
#         "id": case["id"],
#         "desc": case["desc"],
#         "status": status,
#     })
#     print()
#
# # ------ 输出汇总 ------
# print("====== 测试汇总 ======")
# for r in results:
#     print(f"{r['id']} {r['desc']}: {r['status']}")
#
# # 统计通过率
# passed_count = sum(1 for r in results if r["status"] == "PASS")
# total_count = len(results)
# print(f"\n通过率: {passed_count}/{total_count} = {passed_count/total_count*100:.1f}%")