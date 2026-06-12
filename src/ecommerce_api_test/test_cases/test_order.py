#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-11 21:15
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_order.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 订单模块测试


import pytest


@pytest.mark.smoke
def test_create_order_correctly_deducts_stock(order_api, product_api, db_util, test_data):
    """创建订单，商品库存正确扣减"""

    # 创建商品
    product_data = test_data["products"][0]  # 字典列表
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]  # 数据库生成
    initial_stock = product_data["stock"]

    # 下单前数据库校验初始库存
    db_stock_before = db_util.query_one(
        "SELECT stock FROM products WHERE id=%s",
        (product_id,)
    )["stock"]
    assert db_stock_before == initial_stock, "商品初始库存不正确"

    # 创建订单
    order_data = test_data["orders"][0]  # 字典列表
    print(order_data)
    response = order_api.create_order(
        product_id=product_id,
        quantity=order_data["quantity"],
    )
    order_id = order_api.response.json()["id"]
    print(order_id)
    print(response.json())
    print(create_product_response.json())

    # 订单成功
    # 响应校验
    order_api.assert_status_code(200)
    order_api.assert_json_contains({
        "product_id": product_id,
        "quantity": order_data["quantity"],
        "total_price": product_data["price"] * order_data["quantity"],
        "status": "paid"
    })
    order_api.assert_json_has_fields(["id", "user_id"])  # 订单id、用户id

    # 验证库存
    updated_product = product_api.get_product(product_id).json()
    assert updated_product["stock"] == initial_stock - order_data["quantity"]

    # 数据库校验
    # 订单记录
    # 关于数据库建表 当前表均有id， 下一层级的表会写相关表的id用于查询
    # 比如我们用玩具后端 users、products SQL语句写id； order写了user_id、product_id
    db_order = db_util.query_one(
        "SELECT id, user_id, status FROM orders WHERE id=%s",  # 数据库建表id 建表order_items一般才写order_id用于查订单
        (order_id,)
    )
    assert db_order is not None
    assert db_order["status"] == "paid"  # 数据库建表"pending"后端实现创建订单"paid"

    # 订单商品 后端未实现order_items仅用orders实现一个订单购买一种商品
    db_order_items = db_util.query_one(
        "SELECT product_id, quantity, total_price FROM orders WHERE id=%s",
        (order_id,)
    )
    assert db_order_items is not None
    assert db_order_items["product_id"] == product_id
    assert db_order_items["quantity"] == order_data["quantity"]
    assert db_order_items["total_price"] == product_data["price"] * order_data["quantity"]

    # 验证库存正确扣减
    print("接口库存:", updated_product["stock"])  # 99

    db_order_after = db_util.query_one(
        "SELECT stock FROM products WHERE id=%s",
        (product_id,)
    )["stock"]

    print("数据库库存:", db_order_after)  # 100 找到BUG原因 数据库类查询需要rollback
    assert db_order_after == initial_stock - order_data["quantity"], "库存扣减数量错误"

def test_create_order_insufficient_stock(order_api, product_api, test_data):
    product_data = {
        "name": "库存不足的测试商品",
        "price": 100.0,
        "stock": 1
    }
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]

    # 超买
    response = order_api.create_order(
        product_id=product_id, quantity=2
    )
    order_api.assert_status_code(400)
    order_api.assert_error_message("库存不足")

def test_create_order_nonexistent_product(order_api):
    response = order_api.create_order(product_id="999999", quantity=1)
    order_api.assert_status_code(404)
    order_api.assert_error_message("商品不存在")

# def test_create_order_with_multiple_items(order_api, product_api, db_util):
#     product1 = product_api.create_product(name="商品A", price=100.0, stock=100)
#     product2 = product_api.create_product(name="商品B", price=50.0, stock=50)
#
#     response = order_api.create_order_multiple_items(
#         {"product_id": product1["id"], "quantity": 2},
#         {"product_id": product2["id"], "quantity": 1},
#     )
#     assert response.status_code == 200
#     order = response.json()
#     assert order["total_price"] == product1["price"] * product1["quantity"] + \
#         product2["price"] * product2["quantity"]
#     assert len(order["items"]) == 2
#
#     db_items = db_util.query_all(
#         "SELECT * FROM order_items WHERE order_id=%s ORDER BY product_id",
#         (order["id"],)
#     )
#     assert len(db_items) == len(response.json()["items"])
#     assert db_items[0]["product_id"] == product1["product_id"]
#     assert db_items[1]["product_id"] == product2["product_id"]

# # 测试商品夹具
# @pytest.fixture
# def test_product(product_api):
#     resp = product_api.create_product(name="测试商品", price=100.0, stock=100)
#     yield resp.json()
#     # product_api.delete_product(resp.json()["id"])

# def test_get_my_orders(order_api, test_product):
#     order_api.create_order(product_id=test_product["id"], quantity=1)
#     response = order_api.get_orders()
#     assert response.status_code == 200
#     assert len(response.json()) >= 1

def test_get_order_detail(order_api, product_api, test_data):
    product_data = test_data["products"][2]
    create_product_response = product_api.create_product(**product_data)
    product_id = create_product_response.json()["id"]  # 用于下订单

    order_response = order_api.create_order(product_id=product_id, quantity=1)
    order_id = order_response.json()["id"]  # 用于查订单

    response = order_api.get_order(order_id)
    order_api.assert_status_code(200)
    order_api.assert_json_contains({
        "id": order_id,
        "product_id": product_id,
        "quantity": 1,
        "status": "paid"
    })

def test_get_nonexistent_order(order_api):
    response = order_api.get_order(999999)
    order_api.assert_status_code(404)
    order_api.assert_error_message("订单不存在")

def test_create_order_without_auth(user_api):
    response = user_api.post("/orders", json={"product_id":1, "quantity":1})

    print(response.status_code)
    print(response.json())

    user_api.assert_status_code(401)
    # user_api.assert_error_message("无法验证凭据")
    user_api.assert_error_message("Not authenticated")  # 后端没定义 无token的返回信息 fastapi默认Not authenticated

@pytest.mark.xfail(reason="已知缺陷：订单数量为负也创建订单，导致库存增加严重业务BUG")
def test_create_order_negative_quantity(order_api, product_api):
    create_product_response = product_api.create_product(
        name="测试商品",
        price=100.0,
        stock=100
    )
    product_id = create_product_response.json()["id"]

    response = order_api.create_order(
        product_id=product_id,
        quantity=-1,
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 422, "下单数量为负"

    # order_api.assert_status_code(422)
    # order_api.assert_error_message("下单数量必须大于0")

@pytest.mark.xfail(reason="已知缺陷：下单数量为零也创建订单")
def test_create_order_zero_quantity(order_api, product_api):
    create_product_response = product_api.create_product(
        name="测试商品",
        price=100.0,
        stock=100
    )
    product_id = create_product_response.json()["id"]
    response = order_api.create_order(product_id=product_id, quantity=0)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 422, "零数量订单依然成功下单"

    # order_api.assert_status_code(422)
    # order_api.assert_error_message("数量必须大于0")

def test_create_order_float_precision(order_api, product_api):
    """测试浮点数价格计算精度"""

    create_product_response = product_api.create_product(
        name="精度测试商品",
        price=0.1,
        stock=100
    )
    product_id = create_product_response.json()["id"]

    response = order_api.create_order(
        product_id=product_id,
        quantity=3
    )

    print(response.status_code)
    print(response.json())

    assert response.json()["total_price"] == 0.3  # 数据库建表DECIMAL(10,2)

@pytest.mark.xfail(reason="已知缺陷：后端查询订单不检查user_id导致越权访问")
def test_access_other_user_order(order_api, product_api, user_api, test_data):
    """测试越权访问"""

    # fixture 全局用户test_user
    product_resp = product_api.create_product(
        name="越权测试商品",
        price=100.0,
        stock=100
    )
    product_id = product_resp.json()["id"]  # 用于下单
    order_resp = order_api.create_order(product_id=product_id, quantity=1)
    order_id = order_resp.json()["id"]  # 后端定义的用于查询订单

    # 退出登录
    user_api.clear_auth_token()
    user_b = {"username": "user_b", "password": "user_b123"}
    user_api.register(**user_b)  # 解包
    login_resp = user_api.login(**user_b)
    user_api.set_auth_token(login_resp.json()["access_token"])

    # api.close()之前，也就是测试未结束 user_api product_api order_api都在同一个session
    resp = order_api.get_order(order_id)
    print(resp.status_code)
    print(resp.json())  # {'id': 6, 'user_id': 1, 'product_id': 7, 'quantity': 1, 'total_price': 100.0, 'status': 'paid'}

    assert resp.status_code == 404, "后端未检查user_id导致越权访问"


@pytest.mark.xfail(reason="已知缺陷：后端多线程未加锁，存在超卖风险")
def test_concurrent_order_super_sale(order_api, product_api, db_util):
    """测试并发下单超卖问题"""

    import threading

    product_resp = product_api.create_product(
        name="秒杀商品",
        price=100.0,
        stock=1
    )
    product_id = product_resp.json()["id"]


    # 多线程同时放行
    barrier = threading.Barrier(10)

    def order_task():
        try:
            barrier.wait()  # 10个线程同时放行
            resp = order_api.create_order(product_id=product_id, quantity=1)
        except Exception:
            pass

    # 多线程并发下单
    threads = []
    for _ in range(10):
        t = threading.Thread(target=order_task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 预期只有1个订单成功，但后端没有加锁的话，可能会有多个成功
    # 直接查询数据库写入 最准确
    orders = db_util.query_one(
        "SELECT COUNT(*) AS cnt FROM orders WHERE product_id=%s",
        (product_id,)
    )

    assert orders["cnt"] == 1, "多线程并发超卖"

# # 后端未设计功能的测试代码，仅作练习
# def test_cancel_order_restores_stock(order_api, product_api, db_util, test_data):
#     product_data = test_data["products"][0]
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#
#     order_data = test_data["orders"][0]
#     response = order_api.create_order(product_id=product_id, quantity=order_data["quantity"])
#     order_id = response.json()["id"]
#
#     cancel_resp = order_api.cancel_order(order_id=order_id)
#     assert cancel_resp.status_code == 200
#
#     db_stock = db_util.query_one(
#         "SELECT stock FROM products WHERE id=%s",
#         (product_id,)
#     )["stock"]
#     assert db_stock == product_data["stock"]


# # src/ecommerce_api_test/test_cases/test_order.py
# import pytest
#
# @pytest.mark.smoke
# def test_create_order(order_api, product_api, test_data):
#     """测试创建订单（完整流程）"""
#     # 1. 创建商品
#     product_data = test_data["products"][0]
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#     initial_stock = product_data["stock"]
#
#     # 2. 创建订单
#     order_data = test_data["orders"][0]
#     response = order_api.create_order(
#         product_id=product_id,
#         quantity=order_data["quantity"]
#     )
#
#     # 3. 断言订单创建成功
#     order_api.assert_status_code(200)
#     order_api.assert_json_contains({
#         "product_id": product_id,
#         "quantity": order_data["quantity"],
#         "total_price": product_data["price"] * order_data["quantity"],
#         "status": "paid"
#     })
#     order_api.assert_json_has_fields(["id", "user_id"])
#
#     # 4. 验证库存减少
#     updated_product = product_api.get_product(product_id).json()
#     assert updated_product["stock"] == initial_stock - order_data["quantity"]
#
# def test_create_order_insufficient_stock(order_api, product_api, test_data):
#     """测试创建订单时库存不足"""
#     # 1. 创建一个库存为1的商品
#     product_data = {
#         "name": "库存不足测试商品",
#         "price": 100.0,
#         "stock": 1
#     }
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#
#     # 2. 尝试购买2个（应该失败）
#     response = order_api.create_order(product_id=product_id, quantity=2)
#
#     order_api.assert_status_code(400)
#     order_api.assert_error_message("库存不足")
#
# def test_create_order_nonexistent_product(order_api):
#     """测试创建订单时商品不存在"""
#     response = order_api.create_order(product_id=999999, quantity=1)
#
#     order_api.assert_status_code(404)
#     order_api.assert_error_message("商品不存在")
#
# def test_get_order_detail(order_api, product_api, test_data):
#     """测试获取订单详情"""
#     # 1. 创建商品和订单
#     product_data = test_data["products"][2]
#     create_product_response = product_api.create_product(**product_data)
#     product_id = create_product_response.json()["id"]
#
#     create_order_response = order_api.create_order(product_id=product_id, quantity=1)
#     order_id = create_order_response.json()["id"]
#
#     # 2. 获取订单详情
#     response = order_api.get_order(order_id)
#
#     order_api.assert_status_code(200)
#     order_api.assert_json_contains({
#         "id": order_id,
#         "product_id": product_id,
#         "quantity": 1,
#         "status": "paid"
#     })
#
# def test_get_nonexistent_order(order_api):
#     """测试获取不存在的订单"""
#     response = order_api.get_order(999999)
#
#     order_api.assert_status_code(404)
#     order_api.assert_error_message("订单不存在")
#
# def test_create_order_without_auth(user_api):
#     """测试未认证时创建订单（应该失败）"""
#     response = user_api.post("/orders", json={"product_id": 1, "quantity": 1})
#
#     user_api.assert_status_code(401)
#     user_api.assert_error_message("无法验证凭据")