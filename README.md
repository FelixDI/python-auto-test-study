# python-auto-test-study
python自动化测试入门到实战

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
  最终目标：实战 Selenium + Pytest 自动化测试项目

## 目录结构

<!-- PROJECT_STRUCTURE_START -->
```
PythonAutoTest/
├── docs/
│   ├── 01_搭建环境踩坑.md
│   └── 02_测试理论.md
├── src/
│   └── exercises/
│       └── pythonreview/
│           ├── data/
│           │   ├── config.json
│           │   ├── sample.txt
│           │   ├── test_cases.json
│           │   └── test_data.csv
│           ├── 01_variables.py
│           ├── 02_datastructure.py
│           ├── 03_controlflow.py
│           ├── 04_functions.py
│           ├── 05_OOPaboutclass.py
│           ├── combine123_testdataprocess.py
│           ├── combine123_testreports.py
│           ├── combine45_classBaseTest.py
│           └── combine45_runtestcase.py
├── README.md
├── requirements.txt
├── testgitpush.py
└── update_tree.py

6 directories, 19 files
```
<!-- PROJECT_STRUCTURE_END -->



## 学习进度
```
- 01 环境搭建完成 ✅
     miniforge+pycharm+git+github
- 02 Python 基础学习中 🔄
     core python programing 书太厚太全面了跟着敲代码还是学了就忘。
     Python 基础语法回顾（面向自动化测试）目标复习自动化测试高频用到的 Python 语法。

    ### 学习重点
    1.  类与继承：`class BasePage` 封装基础操作，所有页面对象继承
    2.  异常处理：`try-except` 捕获元素定位超时、操作失败
    3.  文件与配置读取：`configparser` 读取 `.ini` 配置文件
    4.  列表/字典/循环：处理测试数据、批量执行用例
```