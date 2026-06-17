# FakeStoreAPI 接口文档（OpenAPI 3.1.0）
## 一、基础信息
- 接口名称：FakeStoreAPI
- 用途：免费电商模拟接口，用于测试与原型开发
- 版本：v2.1.11
- 基础地址：`https://fakestoreapi.com`
- 业务模块：商品(Products)、购物车(Carts)、用户(Users)、认证(Auth)

## 二、商品模块（Products）
### 商品模块（Products）- 1. 获取所有商品
- 请求方法：GET
- 接口路径：`/products`
- 描述：获取全部商品列表
- 成功响应：200，返回商品对象数组
- 失败响应：400，请求参数错误
### 商品模块（Products）- 2. 新增商品
- 请求方法：POST
- 接口路径：`/products`
- 描述：创建一个新商品
- 请求体（application/json）：
  | 字段 | 类型 | 说明 |
  |------|------|------|
  | title | string | 商品名称 |
  | price | number | 商品价格 |
  | description | string | 商品描述 |
  | category | string | 商品分类 |
  | image | string | 商品图片地址 |
- 成功响应：201，返回创建后的商品对象
- 失败响应：400，请求参数错误
### 商品模块（Products）- 3. 获取单个商品（按ID）
- 请求方法：GET
- 接口路径：`/products/{id}`
- 描述：根据商品ID查询商品详情
- 路径参数：
  | 字段 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | id | integer | 是 | 商品ID |
- 成功响应：200，返回单个商品对象
- 失败响应：400，请求参数错误
### 商品模块（Products）- 4. 更新商品（按ID）
- 请求方法：PUT
- 接口路径：`/products/{id}`
- 描述：根据ID更新商品信息
- 路径参数：id（integer，商品ID）
- 请求体：同新增商品字段
- 成功响应：200，返回更新后的商品对象
- 失败响应：400，请求参数错误
### 商品模块（Products）- 5. 删除商品（按ID）
- 请求方法：DELETE
- 接口路径：`/products/{id}`
- 描述：根据ID删除商品
- 路径参数：id（integer，商品ID）
- 成功响应：200，删除成功
- 失败响应：400，请求参数错误

## 三、购物车模块（Carts）
### 购物车模块（Carts）- 1. 获取所有购物车
- 请求方法：GET
- 接口路径：`/carts`
- 描述：获取全部购物车列表
- 成功响应：200，返回购物车对象数组
### 购物车模块（Carts）- 2. 新增购物车
- 请求方法：POST
- 接口路径：`/carts`
- 描述：创建一个新购物车
- 请求体：
  | 字段 | 类型 | 说明 |
  |------|------|------|
  | userId | integer | 用户ID |
  | products | array | 商品列表，包含商品id |
- 成功响应：201，返回创建后的购物车对象
### 购物车模块（Carts）- 3. 获取单个购物车（按ID）
- 请求方法：GET
- 接口路径：`/carts/{id}`
- 路径参数：id（integer，购物车ID）
- 成功响应：200，返回单个购物车对象
### 购物车模块（Carts）- 4. 更新购物车（按ID）
- 请求方法：PUT
- 接口路径：`/carts/{id}`
- 路径参数：id（integer，购物车ID）
- 请求体：同新增购物车
- 成功响应：200，返回更新后的购物车对象
### 购物车模块（Carts）- 5. 删除购物车（按ID）
- 请求方法：DELETE
- 接口路径：`/carts/{id}`
- 路径参数：id（integer，购物车ID）
- 成功响应：200，删除成功

## 四、用户模块（Users）
### 用户模块（Users）- 1. 获取所有用户
- 请求方法：GET
- 接口路径：`/users`
- 成功响应：200，返回用户对象数组
### 用户模块（Users）- 2. 新增用户
- 请求方法：POST
- 接口路径：`/users`
- 请求体：
  | 字段 | 类型 | 说明 |
  |------|------|------|
  | username | string | 用户名 |
  | email | string | 邮箱 |
  | password | string | 密码 |
- 成功响应：201，返回创建后的用户对象
### 用户模块（Users）- 3. 获取单个用户（按ID）
- 请求方法：GET
- 接口路径：`/users/{id}`
- 路径参数：id（integer，用户ID）
- 成功响应：200，返回单个用户对象
### 用户模块（Users）- 4. 更新用户（按ID）
- 请求方法：PUT
- 接口路径：`/users/{id}`
- 路径参数：id（integer，用户ID）
- 请求体：同新增用户
- 成功响应：200，返回更新后的用户对象
### 用户模块（Users）- 5. 删除用户（按ID）
- 请求方法：DELETE
- 接口路径：`/users/{id}`
- 路径参数：id（integer，用户ID）
- 成功响应：200，删除成功

## 五、认证模块（Auth）
### 认证模块（Auth）- 用户登录
- 请求方法：POST
- 接口路径：`/auth/login`
- 描述：用户身份认证，获取token
- 请求体：
  | 字段 | 类型 | 说明 |
  |------|------|------|
  | username | string | 用户名 |
  | password | string | 密码 |
- 成功响应：200，返回 `{ "token": "xxx" }`
- 失败响应：400，请求参数错误

## 六、通用数据模型
### 商品模块（Products）- 商品（Product）数据模型
| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 商品ID |
| title | string | 商品名称 |
| price | number(float) | 商品价格 |
| description | string | 商品描述 |
| category | string | 商品分类 |
| image | string(uri) | 商品图片地址 |
### 购物车模块（Carts）- 购物车（Cart）数据模型
| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 购物车ID |
| userId | integer | 用户ID |
| products | array | 商品列表，关联Product模型 |
### 用户模块（Users）- 用户（User）数据模型
| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 用户ID |
| username | string | 用户名 |
| email | string | 邮箱 |
| password | string | 密码 |