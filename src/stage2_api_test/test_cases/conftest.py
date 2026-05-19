#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 09:07
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : conftest.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : fixture call

import pytest
import requests
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

import time
from pathlib import Path
from datetime import datetime

@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8000"

# @pytest.fixture(autouse=True)
# def clean_database():
#     yield
#
#     engine = create_engine("sqlite:///./test.db",connect_args={"check_same_thread":False})
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     session.execute(text("DELETE FROM users"))
#     session.commit()
#     session.close()


# import pytest
# import requests
# from sqlalchemy import create_engine, text

# # ==================== 数据库引擎 ====================
# @pytest.fixture(scope="module")
# def db_engine():
#     engine = create_engine(
#         "sqlite:///./test.db",
#         connect_args={"check_same_thread": False}
#     )
#     # 核心改动：直接执行SQL建表，不再导入FastAPI模型
#     with engine.connect() as conn:
#         conn.execute(text("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username VARCHAR NOT NULL UNIQUE,
#                 email VARCHAR NOT NULL UNIQUE,
#                 hashed_password VARCHAR NOT NULL,
#                 is_active BOOLEAN DEFAULT 1
#             )
#         """))
#         conn.commit()
#     return engine
#
# # ==================== 数据清理 ====================
# @pytest.fixture(autouse=True)
# def clean_database(db_engine):
#     yield
#     # 在测试函数执行后，用 SQL 清空数据
#     with db_engine.connect() as conn:
#         conn.execute(text("DELETE FROM users"))
#         conn.commit()

# ... 其余 fixture (base_url, auth_token, auth_headers) 保持不变 ...



@pytest.fixture(scope="module")
def auth_token(base_url):
    login_data = {
        "username":"apitest",
        "password":"123456"
    }

    requests.post(
        f"{base_url}/register",
        json={
            "username":login_data["username"],
            "password":login_data["password"],
            "email":"apitest@test.com"
        }
    )

    response = requests.post(f"{base_url}/login",data=login_data)
    assert response.status_code == 200,f"模块级账号登录失败:{response.text}"

    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization":f"Bearer {auth_token}"}      # Bearer {}  与调用之间一定要留空格！！！



@pytest.fixture(scope="session")
def test_result():
    results = []
    yield results

    if not results:
        return

    report_dir = Path(__file__).parent.parent.parent.parent/"reports"
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir/f"api_test_summary_{timestamp}.txt"

    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    total = len(results)

    with open(report_path,"w",encoding="utf-8") as f:
        f.write("="*50+"\n")
        f.write(f" 接口测试汇总报告-{datetime.now()}\n")
        f.write("="*50+"\n\n")

        for r in results:
            icon = "✅"if r["status"]=="passed"else"❌"
            f.write(f"{icon}{r["name"]}({r["duration"]:.2f}s)\n")

        f.write("\n"+"-"*50+"\n")
        f.write(f"总计:{total}通过:{passed}失败:{failed}\n")
        pass_rate =(passed/total*100) if total>0 else 0
        f.write(f"通过率:{pass_rate:.1f}%\n")
    print(f"\n📄TXT报告已生成:{report_path}")


# # 当你给钩子函数加上 hookwrapper=True 时，yield 语句返回的是一个 pluggy.Result 类的实例（也就是 outcome 变量）
# # Result.get_result() 是 pluggy.Result 类的原生方法，作用是：
# # 获取被包装的钩子函数（也就是 pytest 内置的 pytest_runtest_makereport）执行后的返回值
# @pytest.hookimpl(tryfirst=True,hookwrapper=True)
# def pytest_runtest_makereport(item,call):
#     outcome = yield     ## yield会暂停当前函数，等测试执行完后再继续执行后面的代码
#     report = outcome.get_result()   # report 是 pytest.TestReport 类型，定义在 _pytest.reports 模块中。
#
# # # 执行阶段："setup" / "call" / "teardown"
#     if report.when == "call":
#         # item 是 _pytest.nodes.Function 类型，继承自 _pytest.nodes.Node，定义在 _pytest.nodes 模块中。
#         # 它代表单个测试用例节点，每个测试函数（包括参数化生成的每个实例）都会对应一个 Function 对象
#         # 由 pytest 在测试收集阶段创建，包含该测试用例的所有元数据和运行时信息
#         item.user_properties.append("test_result",report.outcome)   #结果
#         # item.user_properties 是一个列表 **，
#         # 是 pytest 专门为用户提供的自定义数据存储容器，用于在测试用例的整个生命周期内传递和保存自定义信息
#         item.user_properties.append("test_duration",report.duration)  #时长

# 标记这是一个pytest钩子实现
# tryfirst=True: 让这个钩子在所有同类型钩子中最先执行
# hookwrapper=True: 将函数标记为钩子包装器，可以在测试执行前后都运行代码
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# 定义pytest_runtest_makereport钩子函数，pytest会自动为每个测试用例的每个执行阶段调用它
# item: 当前测试用例的Function对象，包含测试用例的所有元数据
# call: 测试调用对象，包含执行阶段和异常信息
def pytest_runtest_makereport(item, call):
    """钩子：每个用例执行结束后收集结果"""

    # 交出控制权，让pytest执行实际的测试代码
    # 函数会在这里暂停，直到测试执行完成后再继续执行后面的代码
    outcome = yield

    # 从pluggy.Result对象中获取pytest生成的TestReport实例
    # report包含本次执行阶段的所有结果信息
    report = outcome.get_result()

    # 判断当前执行阶段是否是测试函数主体阶段
    # 跳过setup(前置fixture)和teardown(后置fixture)阶段
    # 确保只记录测试用例本身的执行结果
    if report.when == "call":
        # 从pytest配置对象的内部存储中获取名为"test_results"的列表
        # setdefault方法：如果"test_results"键不存在，就创建它并赋值为空列表
        # 如果键已经存在，就返回已有的列表
        # item.session.config._store是pytest内部的全局字典存储，整个测试会话共享
        results = item.session.config._store.setdefault("test_results", [])

        # 向全局列表中追加当前测试用例的结果字典
        results.append({
            "name": item.nodeid,  # 测试用例的唯一标识（格式：文件路径::函数名[参数]）
            "status": report.outcome,  # 测试结果（passed/failed/skipped/xfailed/xpassed）
            "duration": report.duration,  # 测试执行耗时，单位：秒
        })



# import pytest
# import requests
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
#
# # ==================== 管理基础 URL ====================
# @pytest.fixture(scope="module")
# def base_url():
#     """
#     模块级 fixture：提供被测服务的基础地址
#     作用域 scope="module"：整个测试模块只执行一次
#     """
#     return "http://localhost:8000"
#
#
# # ==================== 数据库清理 (解决数据干扰问题) ====================
# @pytest.fixture(autouse=True)
# def clean_database():
#     """
#     自动执行的函数级 fixture
#     核心作用：每次测试结束后，重置数据库，保证测试数据隔离
#     autouse=True 意味着无需在测试函数参数中显式声明，自动生效
#     """
#     # 前置操作 (yield 之前)：测试函数执行前，什么也不做
#     yield
#     # 后置操作 (yield 之后)：测试函数执行后，删除所有用户数据
#     # 连接到容器内的 SQLite 数据库文件
#     engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     # 直接执行 SQL 删除 users 表中的所有数据
#     session.execute(text("DELETE FROM users"))
#     session.commit()
#     session.close()
#
#
# # ==================== 管理登录 Token ====================
# @pytest.fixture(scope="module")
# def auth_token(base_url):
#     """
#     模块级 fixture：登录一次获取 Token，整个模块的测试复用
#     依赖 base_url fixture，pytest 会自动注入它的返回值
#     """
#     login_data = {
#         "username": "apitest",
#         "password": "123456"
#     }
#
#     # 先注册专用测试账号（如果已存在，忽略 400 错误）
#     requests.post(
#         f"{base_url}/register",
#         json={
#             "username": login_data["username"],
#             "password": login_data["password"],
#             "email": "apitest@test.com"
#         }
#     )
#
#     # 登录获取 Token
#     response = requests.post(f"{base_url}/login", data=login_data)
#     # 确保模块级账号登录成功，否则后续测试无法进行
#     assert response.status_code == 200, f"模块级账号登录失败: {response.text}"
#
#     token_data = response.json()
#     # 返回 Token 字符串
#     return token_data["access_token"]
#
#
# # ==================== 为受保护接口准备的请求头 ====================
# @pytest.fixture
# def auth_headers(auth_token):
#     """
#     函数级 fixture：构造携带 Token 的请求头
#     依赖 auth_token fixture，自动获取 Token
#     """
#     return {"Authorization": f"Bearer {auth_token}"}



# # conftest.py
# import pytest
# import requests
# import time
# from pathlib import Path
# from datetime import datetime
#
# # ==================== 原有 fixture ====================
# @pytest.fixture(scope="module")
# def base_url():
#     return "http://localhost:8000"
#
# @pytest.fixture(scope="module")
# def auth_token(base_url):
#     login_data = {"username": "apitest", "password": "123456"}
#     requests.post(f"{base_url}/register", json={
#         "username": login_data["username"],
#         "password": login_data["password"],
#         "email": "apitest@test.com"
#     })
#     response = requests.post(f"{base_url}/login", data=login_data)
#     assert response.status_code == 200, f"模块级账号登录失败: {response.text}"
#     return response.json()["access_token"]
#
# @pytest.fixture
# def auth_headers(auth_token):
#     return {"Authorization": f"Bearer {auth_token}"}
#
# # ==================== 测试结果收集与 TXT 报告生成 ====================
# @pytest.fixture(scope="session")
# def test_results():
#     """收集整个测试会话的所有用例结果"""
#     results = []
#     yield results
#     # ---- 测试全部结束后，自动生成 TXT 报告 ----
#     if not results:
#         return
#     report_dir = Path(__file__).parent.parent.parent.parent / "reports"
#     report_dir.mkdir(exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     report_path = report_dir / f"api_test_summary_{timestamp}.txt"
#
#     passed = sum(1 for r in results if r["status"] == "passed")
#     failed = sum(1 for r in results if r["status"] == "failed")
#     total = len(results)
#
#     with open(report_path, "w", encoding="utf-8") as f:
#         f.write("=" * 50 + "\n")
#         f.write(f"  接口测试汇总报告 - {datetime.now()}\n")
#         f.write("=" * 50 + "\n\n")
#         for r in results:
#             icon = "✅" if r["status"] == "passed" else "❌"
#             f.write(f"{icon} {r['name']} ({r['duration']:.2f}s)\n")
#         f.write("\n" + "-" * 50 + "\n")
#         f.write(f"总计: {total}  通过: {passed}  失败: {failed}\n")
#         pass_rate = (passed / total * 100) if total > 0 else 0
#         f.write(f"通过率: {pass_rate:.1f}%\n")
#     print(f"\n📄 TXT 报告已生成: {report_path}")
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """钩子：每个用例执行结束后收集结果"""
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call":
#         # 把结果追加到 test_results fixture 的列表中
#         results = item.session.config._store.setdefault("test_results", [])
#         results.append({
#             "name": item.nodeid,
#             "status": report.outcome,
#             "duration": report.duration,
#         })