#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-14 15:40
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : combine45_runtestcase.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 综合练习1:封装一个测试用例执行函数

import functools
import time


def test_case(func):
    # 复制 func 的元数据到 wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[开始]{func.__name__}")
        start = time.time()

        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"[通过]{func.__name__}({elapsed:.2f}s)")
            return result
        except AssertionError as e:
            elapsed = time.time() - start
            print(f"[失败]{func.__name__}({elapsed:.2f}s) - 断言失败:{e}")
            raise
        except Exception as e:
            elapsed = time.time() - start
            print(f"[异常]{func.__name__}({elapsed:.2f}s)- {type(e).__name__}:{e}")
            raise

    return wrapper

@test_case
def test_login_success():
    assert 1+1 == 2, "数学崩了"

@test_case
def test_login_fail():
    try:
        int('abc')
    except ValueError:
        pass                # 预期的异常发生了
    else:
        raise AssertionError("应该抛出 ValueError,但没有抛出")

# test_login_success()
# test_login_fail()

def run_test(*test_funcs):
    passed = 0
    failed = 0

    for func in test_funcs:
        try:
            func()
            passed += 1
        except:
            failed += 1

    print(f"\n总计:{passed + failed},通过:{passed},失败:{failed}")
    return {"passed":passed,"failed":failed}

run_test(test_login_success,test_login_fail)


#
# ============================================
# 实战1：封装一个测试用例执行函数（修正版）
# ============================================
# import functools
# import time
#
# # ------ 装饰器：给用例添加计时和日志 ------
# def test_case(func):
#     """装饰器：自动记录用例执行耗时和状态"""
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"[开始] {func.__name__}")
#         start = time.time()
#         try:
#             result = func(*args, **kwargs)
#             elapsed = time.time() - start
#             print(f"[通过] {func.__name__} ({elapsed:.2f}s)")
#             return result
#         except AssertionError as e:
#             elapsed = time.time() - start
#             print(f"[失败] {func.__name__} ({elapsed:.2f}s) - 断言失败: {e}")
#             raise
#         except Exception as e:
#             elapsed = time.time() - start
#             print(f"[异常] {func.__name__} ({elapsed:.2f}s) - {type(e).__name__}: {e}")
#             raise
#     return wrapper
#
#
# # ------ 使用装饰器执行测试 ------
# @test_case
# def test_login_success():
#     """模拟测试：登录成功"""
#     # 模拟操作...
#     assert 1 + 1 == 2, "数学崩了"
#
# @test_case
# def test_login_fail():
#     """模拟测试：登录失败，预期抛出 ValueError"""
#     try:
#         int("abc")
#     except ValueError:
#         # 预期捕获到异常，测试通过
#         pass
#     else:
#         # 如果没有抛出异常，则测试失败
#         raise AssertionError("应该抛出 ValueError，但没有抛出")
#
#
# # ------ 封装一个批量执行函数 ------
# def run_tests(*test_funcs):
#     """批量执行多个测试函数，返回统计结果"""
#     passed = 0
#     failed = 0
#     for func in test_funcs:
#         try:
#             func()
#             passed += 1
#         except:
#             failed += 1
#     print(f"\n总计: {passed+failed}, 通过: {passed}, 失败: {failed}")
#     return {"passed": passed, "failed": failed}
#
# # 运行示例
# run_tests(test_login_success, test_login_fail)