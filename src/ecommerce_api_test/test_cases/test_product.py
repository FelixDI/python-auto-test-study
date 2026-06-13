#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-06-11 19:19
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : test_product.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 商品模块测试


import pytest


@pytest.mark.smoke
def test_create_product(product_api, db_util, test_data):
    product_data = test_data["products"][0]  # 三个商品的字典列表
    response = product_api.create_product(
        name=product_data["name"],
        price=product_data["price"],
        stock=product_data["stock"],
    )
    product_id = response.json()["id"]

    print(response.json())

    product_api.assert_status_code(200)
    product_api.assert_json_contains({
        "name": product_data["name"],
        "price": product_data["price"],
        "stock": product_data["stock"],
    })
    product_api.assert_json_has_fields(["id"])

    # 数据库校验
    db_product = db_util.query_one(
        "SELECT name, price, stock FROM products WHERE id=%s",
        (product_id,)
    )
    print(db_product)
    assert db_product is not None
    assert db_product["name"] == product_data["name"]
    assert db_product["price"] == product_data["price"]
    assert db_product["stock"] == product_data["stock"]

def test_list_products(product_api, test_data):
    response = product_api.list_products()

    product_api.assert_status_code(200)
    products = product_api.response.json()
    assert isinstance(products, list)
    assert len(products) >= 0

def test_get_product_detail(product_api, test_data):
    product_data = test_data["products"][1]
    create_response = product_api.create_product(**product_data)
    product_id = create_response.json()["id"]  # 后端返回的json数据，包含数据库自动生成id

    response = product_api.get_product(product_id)
    product_api.assert_status_code(200)
    product_api.assert_json_contains({
        "name": product_data["name"],
        "price": product_data["price"],
        "stock": product_data["stock"],
    })

def test_get_nonexistent_product(product_api):
    response = product_api.get_product(999999)  # 夹具只是包装成ProductApi的实例，并未进行create_product
    product_api.assert_status_code(404)
    product_api.assert_error_message("商品不存在")

def test_create_product_without_auth(user_api, test_data):
    """测试未认证时创建商品（应该失败）"""
    product_data = test_data["products"][0]

    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    # 没有带 Token 时，FastAPI 自动返回 "detail": "Not authenticated"
    # 使用未认证的客户端
    response = user_api.post("/products", json=product_data)

    print(user_api.response.status_code)  # pytest 只在“测试失败/异常时”才显示 print（默认 capture 机制）
    print(user_api.response.text)

    user_api.assert_status_code(401)
    # user_api.assert_error_message("无法验证凭据")
    user_api.assert_error_message("Not authenticated")

def test_create_product_with_invalid_auth(user_api, test_data):
    product_data = test_data["products"][2]

    user_api.set_auth_token("invalid_token")  # 虽然有token但是格式不对
    response = user_api.post(endpoint="/products", json=product_data)

    print(response.status_code)
    print(response.json())

    user_api.assert_status_code(401)
    user_api.assert_error_message("无法验证凭据")

@pytest.mark.xfail(reason="已知缺陷：商品价格为负数，依然正常创建商品")
def test_create_product_negative_price(product_api):
    response = product_api.create_product(
        name="负数价格商品",
        price=-999.0,
        stock=100,
    )
    print(response.status_code)
    print(response.json())

    assert response.status_code == 422, "价格为负数也成功创建商品"
    # 期望行为
    # product_api.assert_status_code(422)
    # product_api.assert_error_message("价格必须大于0")

@pytest.mark.xfail(reason="已知缺陷：商品价格为零，依然正常创建商品")
def test_create_product_zero_price(product_api):
    response = product_api.create_product(
        name="零价商品",
        price=0,
        stock=100,
    )
    print(response.status_code)
    print(response.json())

    assert response.status_code == 422, "价格为0也成功创建商品"

    # product_api.assert_status_code(422)
    # product_api.assert_error_message("价格必须大于0")

@pytest.mark.xfail(reason="已知缺陷：库存为负的商品依然被创建")
def test_create_product_negative_stock(product_api):
    response = product_api.create_product(
        name="负库存商品",
        price=100.0,
        stock=-100,
    )
    print(response.status_code)
    print(response.json())

    assert response.status_code == 422, "库存为负的商品被创建"
    # product_api.assert_status_code(422)
    # product_api.assert_error_message("库存必须大于等于0")

# # src/ecommerce_api_test/test_cases/test_product.py
# import pytest
#
# @pytest.mark.smoke
# def test_create_product(product_api, test_data):
#     """测试创建商品（需要认证）"""
#     product_data = test_data["products"][0]
#
#     response = product_api.create_product(
#         name=product_data["name"],
#         price=product_data["price"],
#         stock=product_data["stock"]
#     )
#
#     product_api.assert_status_code(200)
#     product_api.assert_json_contains({
#         "name": product_data["name"],
#         "price": product_data["price"],
#         "stock": product_data["stock"]
#     })
#     product_api.assert_json_has_fields(["id"])
#
# def test_list_products(product_api):
#     """测试获取商品列表"""
#     response = product_api.list_products()
#
#     product_api.assert_status_code(200)
#     products = product_api.response.json()
#     assert isinstance(products, list)
#     assert len(products) >= 0
#
# def test_get_product_detail(product_api, test_data):
#     """测试获取单个商品详情"""
#     # 先创建一个商品
#     product_data = test_data["products"][1]
#     create_response = product_api.create_product(**product_data)
#     product_id = create_response.json()["id"]
#
#     # 获取商品详情
#     response = product_api.get_product(product_id)
#
#     product_api.assert_status_code(200)
#     product_api.assert_json_contains({
#         "id": product_id,
#         "name": product_data["name"],
#         "price": product_data["price"],
#         "stock": product_data["stock"]
#     })
#
# def test_get_nonexistent_product(product_api):
#     """测试获取不存在的商品"""
#     response = product_api.get_product(999999)
#
#     product_api.assert_status_code(404)
#     product_api.assert_error_message("商品不存在")
#
# def test_create_product_without_auth(user_api, test_data):
#     """测试未认证时创建商品（应该失败）"""
#     product_data = test_data["products"][0]
#
#     # 使用未认证的客户端
#     response = user_api.post("/products", json=product_data)
#
#     user_api.assert_status_code(401)
#     user_api.assert_error_message("无法验证凭据")