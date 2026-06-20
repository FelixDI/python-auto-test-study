# python-auto-test-study
python自动化测试入门到项目实战

## 学习路线图

```mermaid
flowchart LR
    A[一阶段<br>Python 测试专用基础<br>] --> B[二阶段<br>接口自动化核心<br>]
    B --> C[三阶段<br>UI 自动化与项目实战<br>]
    C --> D[面试冲刺<br>背诵 + 回顾]
    
    A -.-> E[工具体系]
    E -.-> F[Requests + Pytest]
    F -.-> G[Selenium / Playwright]
    
    D --> H[准备求职<br>简历 + 项目 + 面试题]
```


# Python 自动化测试学习
  最终目标：接口测试、UI测试、AI测试提效、测试智能体

## 目录结构

<!-- PROJECT_STRUCTURE_START -->
```
PythonAutoTest/
├── docs/
│   ├── 01_搭建环境踩坑.md
│   ├── 02_测试理论.md
│   ├── 03_补充.md
│   ├── 04_UI测试POM踩坑.md
│   └── 05_dify踩坑.md
├── reports/
│   ├── playwright/
│   │   ├── saucedemo_after_login.png
│   │   ├── saucedemo_homepage.png
│   │   ├── saucedemo_order_complete.png
│   │   └── saucedemo_products.png
│   ├── api_test_report.html
│   ├── stage2_final_report.html
│   └── test_report_20260515_204741.txt
├── src/
│   ├── ecommerce_api_test/
│   │   ├── apis/
│   │   │   ├── order_api.py
│   │   │   ├── product_api.py
│   │   │   └── user_api.py
│   │   ├── common/
│   │   │   └── base_api.py
│   │   ├── data/
│   │   │   └── test_data.json
│   │   ├── db/
│   │   │   └── schema.sql
│   │   ├── test_cases/
│   │   │   ├── test_order.py
│   │   │   ├── test_product.py
│   │   │   └── test_user.py
│   │   ├── utils/
│   │   │   └── db_util.py
│   │   └── conftest.py
│   ├── exercises/
│   │   └── pythonreview/
│   │       ├── data/
│   │       │   ├── config.json
│   │       │   ├── sample.txt
│   │       │   ├── test_cases.json
│   │       │   └── test_data.csv
│   │       ├── 01_variables.py
│   │       ├── 02_datastructure.py
│   │       ├── 03_controlflow.py
│   │       ├── 04_functions.py
│   │       ├── 05_OOPaboutclass.py
│   │       ├── combine123_testdataprocess.py
│   │       ├── combine123_testreports.py
│   │       ├── combine45_classBaseTest.py
│   │       ├── combine45_runtestcase.py
│   │       ├── runner.py
│   │       └── utils.py
│   ├── project_ecommerce/
│   │   ├── conftest.py
│   │   ├── db_example.py
│   │   ├── test_auth.py
│   │   ├── test_negative.py
│   │   ├── test_orders.py
│   │   ├── test_products.py
│   │   └── test_with_allure.py
│   ├── saucedemo_ui_test/
│   │   ├── common/
│   │   │   └── base_page.py
│   │   ├── components/
│   │   │   └── menu_component.py
│   │   ├── data/
│   │   │   └── users.json
│   │   ├── pages/
│   │   │   ├── cart_page.py
│   │   │   ├── checkout_page.py
│   │   │   ├── login_page.py
│   │   │   └── products_page.py
│   │   ├── testcases/
│   │   │   ├── test_cart.py
│   │   │   ├── test_checkout.py
│   │   │   ├── test_login.py
│   │   │   ├── test_menu_functionality.py
│   │   │   └── test_products.py
│   │   └── conftest.py
│   ├── stage1_pytest_core/
│   │   ├── data/
│   │   │   └── test_cases.json
│   │   └── test_cases/
│   │       ├── conftest.py
│   │       ├── test_basic.py
│   │       ├── test_fixture.py
│   │       ├── test_markers.py
│   │       ├── test_mock_external.py
│   │       ├── test_mock.py
│   │       ├── test_parametrize.py
│   │       ├── test_unittest_demo.py
│   │       └── test_user_api.py
│   ├── stage2_api_test/
│   │   ├── server/
│   │   │   ├── app/
│   │   │   │   └── main.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   └── test_cases/
│   │       ├── conftest.py
│   │       ├── test_auth_fixture.py
│   │       ├── test_auth.py
│   │       ├── test_integration.py
│   │       ├── test_mock_external.py
│   │       ├── test_param_auth.py
│   │       ├── test_schema.py
│   │       └── test_users_crud.py
│   ├── stage3_ui_test/
│   │   ├── conftest.py
│   │   ├── test_ai_generated.py
│   │   ├── test_saucedemo_allure.py
│   │   ├── test_saucedemo_assert.py
│   │   ├── test_saucedemo_flow.py
│   │   ├── test_saucedemo_login.py
│   │   ├── test_saucedemo_selenium.py
│   │   ├── test_saucedemo.py
│   │   └── testcases_ai_generated.md
│   └── stage4_ai_test/
│       └── dify/
│           ├── examples/
│           │   └── api_test/
│           │       ├── demo_code.py
│           │       ├── demo_input.txt
│           │       └── demo_testcase.md
│           ├── knowledge_base/
│           │   ├── common_rules/
│           │   │   ├── 测试用例设计规范.md
│           │   │   ├── 测试报告模板.md
│           │   │   └── Pytest 代码编写规范.md
│           │   └── fakestoreapi_api/
│           │       ├── fakestoreapi-openapi.json
│           │       ├── FakeStoreAPI接口文档.md
│           │       └── FakeStoreAPI补充说明.md
│           └── workflows/
│               └── ai_test_workflow.yml
├── docker-compose.yml
├── Jenkinsfile
├── pytest.ini
├── README.md
├── requirements.txt
├── testgitpush.py
└── update_tree.py

38 directories, 105 files
```
<!-- PROJECT_STRUCTURE_END -->



## 进度
```
- 01 环境搭建完成 ✅
     miniforge+pycharm+git+github
     docker desktop(fastapi+mysql+Jenkins)
     gitclone到本地启动dify容器，配置deepseek-v4-pro API key
     
- 02 Python 基础学习 ✅
     core python programing 书本代码学习效率较低
     Python 基础语法回顾（面向自动化测试）目标复习自动化测试高频用到的 Python 语法。

- 03 电商接口测试项目实战 ✅
     Pytest · Requests · pymysql · Docker · Jenkins · GitHub Actions · Allure
     AOP重构 + 数据库校验
     
- 04 SauceDemo项目实战UI自动化测试 ✅
     Playwright · Pytest · pytest-playwright · GitHub Actions · Allure
     playwright实战 (POM + component object)
     selenium代码快速上手

- 05 AI测试
     AI测试提效 dify+DeepSeekv4pro -> ai_test_workflow.yml
     创建知识库、工作流，实现FakeStoreAPI接口测试网站用例/代码自动生成  ✅
     
     AI测试智能体：
     Hermes智能体 自我进化优势突出，但目前尚不稳定 不能落地企业场景
     
     搭建可控智能体架构  LLM + Harness Engineering
     LangGraph
        ↓
     控制Agent流程

     LangChain
        ↓
     调用LLM/RAG/Tool Skill（本质就是@tool python代码）

     Playwright
        ↓
     操作浏览器
    
     pytest
        ↓
     执行测试
    
       MCP （代码实现MCP服务器 大脑和手之间的“通用翻译官”和“连接中枢”）
        ↓
     连接外部工具
     
 
     Locust 压力测试
```

## 测试报告


#### API test: src/ecommerce_api_test
[ecommerce Allure api测试报告](https://felixdi.github.io/python-auto-test-study/api-allure-report/)


#### UI test: src/saucedemo_ui_test
[SauceDemo Allure UI测试报告](https://felixdi.github.io/python-auto-test-study/ui-allure-report/)