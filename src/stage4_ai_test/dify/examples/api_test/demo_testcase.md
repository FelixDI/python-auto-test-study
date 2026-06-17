## 一、正常流程场景用例

| 用例ID | 用例名称 | 请求方式 | 接口路径 | 入参说明 | 预期结果 |
|--------|----------|----------|----------|----------|----------|
| TC-PROD-001 | 获取所有商品列表 | GET | /products | 无请求体，无查询参数 | 1. 状态码 200<br>2. 响应体为非空 JSON 数组<br>3. 数组元素包含 id、title、price、description、category、image 字段<br>4. price 为 number 类型 |
| TC-PROD-002 | 获取单个商品（ID=1） | GET | /products/1 | 路径参数 id=1 | 1. 状态码 200<br>2. 响应体为 JSON 对象<br>3. 包含完整字段：id=1、title、price、description、category、image<br>4. 各字段类型符合 Product 模型 |
| TC-PROD-003 | 获取单个商品（ID最大已知值） | GET | /products/20 | 路径参数 id=20（已知最大有效ID） | 1. 状态码 200<br>2. 响应体为 JSON 对象<br>3. id=20，其他字段完整 |
| TC-PROD-004 | 新增商品（完整合法字段） | POST | /products | 请求头：Content-Type: application/json<br>请求体：<br>{"title": "Test Product", "price": 29.99, "description": "A test item", "category": "electronics", "image": "https://example.com/img.jpg"} | 1. 状态码 201<br>2. 响应体为 JSON 对象<br>3. 返回字段与请求体一致<br>4. 自动生成 id 字段，值为正整数<br>5. 返回的 price 类型为 number |
| TC-PROD-005 | 新增商品（price为整数） | POST | /products | 请求头：Content-Type: application/json<br>请求体：<br>{"title": "Integer Price", "price": 100, "description": "test", "category": "books", "image": "https://example.com/book.jpg"} | 1. 状态码 201<br>2. 返回 id 字段<br>3. price 值为 100（可为整数） |
| TC-PROD-006 | 新增商品（price为小数） | POST | /products | 请求头：Content-Type: application/json<br>请求体：<br>{"title": "Float Price", "price": 0.99, "description": "test", "category": "clothing", "image": "https://example.com/cloth.jpg"} | 1. 状态码 201<br>2. price 值为 0.99 |
| TC-PROD-007 | 更新商品（ID=1，完整合法字段） | PUT | /products/1 | 路径参数 id=1<br>请求头：Content-Type: application/json<br>请求体：<br>{"title": "Updated Product", "price": 49.99, "description": "Updated description", "category": "updated-cat", "image": "https://example.com/updated.jpg"} | 1. 状态码 200<br>2. 响应体为 JSON 对象<br>3. 所有字段更新为请求体新值<br>4. id 保持为 1 |
| TC-PROD-008 | 删除商品（ID=1） | DELETE | /products/1 | 路径参数 id=1 | 1. 状态码 200<br>2. 响应体为 JSON 对象（通常返回被删除的资源或空对象） |

## 二、异常入参场景用例

### 2.1 路径参数异常

| 用例ID | 用例名称 | 请求方式 | 接口路径 | 入参说明 | 预期结果 |
|--------|----------|----------|----------|----------|----------|
| TC-PROD-009 | 获取单个商品-ID为字符串 | GET | /products/abc | 路径参数 id="abc" | 状态码 400 |
| TC-PROD-010 | 获取单个商品-ID为特殊字符 | GET | /products/@#$ | 路径参数 id="@#$" | 状态码 400 |
| TC-PROD-011 | 获取单个商品-ID为浮点数 | GET | /products/1.5 | 路径参数 id=1.5 | 状态码 400 |
| TC-PROD-012 | 获取单个商品-ID为负数 | GET | /products/-1 | 路径参数 id=-1 | 状态码 400 |
| TC-PROD-013 | 获取单个商品-ID为零 | GET | /products/0 | 路径参数 id=0 | 状态码 400（或返回特定行为，依据接口规范预期400） |
| TC-PROD-014 | 获取单个商品-ID超大整数值 | GET | /products/999999999999 | 路径参数 id=999999999999 | 状态码 400 |
| TC-PROD-015 | 更新商品-ID为字符串 | PUT | /products/xyz | 路径参数 id="xyz"<br>请求体：合法JSON | 状态码 400 |
| TC-PROD-016 | 删除商品-ID为负数 | DELETE | /products/-5 | 路径参数 id=-5 | 状态码 400 |

### 2.2 请求体异常

| 用例ID | 用例名称 | 请求方式 | 接口路径 | 入参说明 | 预期结果 |
|--------|----------|----------|----------|----------|----------|
| TC-PROD-017 | 新增商品-缺失title字段 | POST | /products | 请求体：<br>{"price": 10.0, "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-018 | 新增商品-缺失price字段 | POST | /products | 请求体：<br>{"title": "No Price", "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-019 | 新增商品-缺失description字段 | POST | /products | 请求体：<br>{"title": "No Desc", "price": 5.0, "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-020 | 新增商品-缺失category字段 | POST | /products | 请求体：<br>{"title": "No Cat", "price": 5.0, "description": "d", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-021 | 新增商品-缺失image字段 | POST | /products | 请求体：<br>{"title": "No Img", "price": 5.0, "description": "d", "category": "c"} | 状态码 400 |
| TC-PROD-022 | 新增商品-请求体为空对象 | POST | /products | 请求体：{} | 状态码 400 |
| TC-PROD-023 | 新增商品-请求体为空 | POST | /products | 无请求体或不发送body | 状态码 400 |
| TC-PROD-024 | 新增商品-请求体为非JSON格式 | POST | /products | 请求头：Content-Type: application/json<br>请求体：纯文本字符串 "not a json" | 状态码 400 |
| TC-PROD-025 | 新增商品-price为字符串类型 | POST | /products | 请求体：<br>{"title": "Bad Price", "price": "free", "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-026 | 新增商品-title为整数类型 | POST | /products | 请求体：<br>{"title": 12345, "price": 10.0, "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400（预期title应为字符串） |
| TC-PROD-027 | 新增商品-price为null | POST | /products | 请求体：<br>{"title": "Null Price", "price": null, "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |
| TC-PROD-028 | 新增商品-多余未知字段 | POST | /products | 请求体包含合法全字段 + "foo": "bar" | 状态码 201（预期忽略未知字段） 或 400（取决于接口严格性，本用例为监控） |
| TC-PROD-029 | 更新商品-请求体缺失price | PUT | /products/1 | 路径参数 id=1<br>请求体：<br>{"title": "Update", "description": "d", "category": "c", "image": "https://a.com/1.jpg"} | 状态码 400 |

## 三、边界值场景用例

| 用例ID | 用例名称 | 请求方式 | 接口路径 | 入参说明 | 预期结果 |
|--------|----------|----------|----------|----------|----------|
| TC-PROD-030 | 新增商品-price为0 | POST | /products | 请求体：price=0 | 状态码 201（或400，若业务禁止免费商品） |
| TC-PROD-031 | 新增商品-price为极大正数 | POST | /products | 请求体：price=999999999.99 | 状态码 201 或 400（取决于数值范围限制） |
| TC-PROD-032 | 新增商品-price为负数 | POST | /products | 请求体：price=-10.50 | 状态码 400（多数业务拒绝负价格） |
| TC-PROD-033 | 新增商品-title为空字符串 | POST | /products | 请求体：title="" | 状态码 201 或 400（取决于空串是否视为有效） |
| TC-PROD-034 | 新增商品-description为空字符串 | POST | /products | 请求体：description="" | 状态码 201 或 400 |
| TC-PROD-035 | 新增商品-title超长字符串（10000字符） | POST | /products | 请求体：title使用重复字符生成10000长度 | 状态码 201 或 400（若有限制长度） |
| TC-PROD-036 | 新增商品-description超长字符串（10000字符） | POST | /products | 请求体：description使用重复字符生成10000长度 | 状态码 201 或 400 |
| TC-PROD-037 | 新增商品-image为无效URL格式 | POST | /products | 请求体：image="not-a-valid-url" | 状态码 201（若不校验URI格式）或 400（若严格校验） |
| TC-PROD-038 | 获取单个商品-ID为最大整数边界 | GET | /products/2147483647 | 路径参数 id=2147483647（32位int边界） | 状态码 200 或 400（若不存在则可能400） |

## 四、幂等性与其他建议用例

| 用例ID | 用例名称 | 请求方式 | 接口路径 | 入参说明 | 预期结果 |
|--------|----------|----------|----------|----------|----------|
| TC-PROD-039 | 删除同一商品两次（幂等性） | DELETE | /products/1 | 第一次删除后，再次对同一ID执行DELETE | 第一次 200；第二次行为需观察（可能 200、404 或 400，基于实际实现确认） |
| TC-PROD-040 | 重复更新同一商品（幂等性） | PUT | /products/1 | 使用相同请求体连续PUT两次 | 两次均返回 200，响应数据一致 |
| TC-PROD-041 | 获取所有商品响应时间基线 | GET | /products | 无 | 响应时间 < 2000ms（设定性能基线） |
