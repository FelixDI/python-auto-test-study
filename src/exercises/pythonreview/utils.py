#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-15 09:57
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : utils.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 工具函数集中在一起，覆盖：JSON/CSV/TXT读取、日志配置、目录创建/清理（os模块）、报告生成


import json
import csv
import logging
import os
from pathlib import Path
from datetime import datetime

def setup_logging(level="INFO"):
    logging.basicConfig(
        level = getattr(logging, level),
        format = "%(asctime)s[%(levelname)s]%(message)s",
        datefmt = "%H:%M:%S",
    )
# def setup_logging(level_name="INFO"):  # 参数名改为 level_name
#     level_value = getattr(logging, level_name)  # 新变量名
#     logging.basicConfig(
#     level=level_value
#     ...
#     )
#     # 这样既保留了原字符串，又有了整数值

# logging 模块内部定义的字段名 举例说明：
# %(asctime)s	str	可读时间
# %(created)f	float	时间戳
# %(msecs)d	int	毫秒部分

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:       # 以只读模式打开一个文件，并使用 UTF-8 编码
        return json.load(f)

def load_csv_data(csv_path):
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)   # 字典 读取器对象
        # print(reader.fieldnames)  # ['id', 'username', 'password', 'expected_code']

        for row in reader:   # csv.DictReader迭代器默认从第二行（数据行）开始返回
            # print(row)   # 一个字典
            if "expected_code" in row:
                row["expected_code"] = int(row["expected_code"])
            data.append(row)

    return data

#next() 是 Python 的内置函数，用于从迭代器中获取下一个元素
# next(iterator, default)  # 如果设置默认值，迭代结束，返回默认值而不抛出异常
# csv.DictReader 的简化版实现
# class DictReader:
#     def __init__(self, csv_file):
#         self.reader = csv.reader(csv_file)   #csv.reader()内部实现返回一个list元素迭代器  一个list存放的就是 文件的一行数据
#         # 关键：在初始化时就读取了第一行作为字段名
#         self.fieldnames = next(self.reader)  # 消耗掉第一行
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         # 每次迭代时，从第二行开始读取
#         row = next(self.reader)  # 这里的 next 是从第二行开始
#         if row is None:
#             raise StopIteration
#         # 将字段名和当前行数据配对成字典
#         zip()结果[('id', 'TC001'), ('username', 'admin'), ('password', '123456'), ('expected_code', '200')]
#         return dict(zip(self.fieldnames, row))  # zip() 将两个list配对  返回迭代器
#         # 每次产生一个字典 形如 {'id': 'TC001', 'username': 'admin', 'password': '123456', 'expected_code': '200'}



def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_data_dir():
    # __file__    Python 内置变量，表示当前文件utils.py的完整路径.../src/exercises/pythonreview/utils.py
    return Path(__file__).parent/"data"     #.parent 只是回到父目录，但父目录里有很多东西，所以需要用/"data" 指定具体

def get_reports_dir():
    project_root = Path(__file__).parent.parent.parent.parent
    reports_dir = project_root/"reports"
    return reports_dir


def ensure_dir_os(dir_path):
    os.makedirs(dir_path, exist_ok=True)    # exist_ok=True 目录存在也不报错   False反之，目录存在会报错
    # 执行后目录一定存在

def clean_old_reports(reports_dir, keep_days=7):
    now = datetime.now().timestamp()   # 计算机元年 时间戳
    # if not os.path.exists(reports_dir):   # 冗余
    #     return

    for filename in os.listdir(reports_dir):
        file_path = os.path.join(reports_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if (now - file_mtime) > keep_days*86400:
                os.remove(file_path)


def generate_txt_report(results, report_path):
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed
    pass_rate = (passed/total*100)if total>0 else 0     # 避免total==0 报错ZeroDivisionError: division by zero

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write(f" 测试报告-{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")
        f.write("="*50 + "\n\n")

        for r in results:
            status = r["status"]
            line = f"[{status}]{r["id"]}:{r["desc"]}"
            if r.get("error"):
                line += f"(错误:{r["error"]})"
            f.write(line+"\n")

        f.write("\n" + "-"*50 + "\n")
        f.write(f"总计:{total}通过:{passed}失败:{failed}")
        f.write(f"通过率:{pass_rate:.1f}%\n")
        f.write("-"*50 + "\n")



# utils.py - 测试工具模块（增强版）
# import json
# import csv
# import logging
# import os
# import shutil
# shutil 做更高级的批量操作  shutil.rmtree() 是整个目录直接删掉
# from pathlib import Path
# from datetime import datetime
#
# # ==================== 1. 日志配置 ====================
# def setup_logging(level="INFO"):
#     logging.basicConfig(
#         level=getattr(logging, level),
#         format="%(asctime)s [%(levelname)s] %(message)s",
#         datefmt="%H:%M:%S",
#     )
#
# # ==================== 2. 读取 JSON 配置/数据 ====================
# def load_json(file_path):
#     """读取任意 JSON 文件，返回 Python 对象"""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)
#
# # ==================== 3. 读取 CSV 测试数据 ====================
# def load_csv_data(csv_path):
#     """读取 CSV，返回列表，每行是字典（自动转换 expected_code）"""
#     data = []
#     with open(csv_path, "r", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if "expected_code" in row:
#                 row["expected_code"] = int(row["expected_code"])
#             data.append(row)
#     return data
#
# # ==================== 4. 读取 TXT 文本文件 ====================
# def read_txt(file_path):
#     """读取纯文本文件，返回字符串"""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()
#
# # ==================== 5. 路径工具 ====================
# def get_data_dir():
#     """返回 data 目录的绝对路径（与本文件同级 data/）"""
#     return Path(__file__).parent / "data"
#
# def get_reports_dir():
#     """返回 reports 目录（项目根目录下的 reports/）"""
#     # 这里我们把报告统一输出到项目根下的 reports/ ，也可以改成 data/reports/
#     project_root = Path(__file__).parent.parent.parent  # 向上三层到 python-auto-test-study/
#     reports_dir = project_root / "reports"
#     return reports_dir
#
# # ==================== 6. 使用 os 模块创建目录 ====================
# def ensure_dir_os(dir_path):
#     """使用 os.makedirs 创建目录（等效于 mkdir -p）"""
#     os.makedirs(dir_path, exist_ok=True)
#
# # ==================== 7. 删除旧报告文件 ====================
# def clean_old_reports(reports_dir, keep_days=7):
#     """
#     删除 reports_dir 中超过 keep_days 天的文件
#     （这里为了演示，直接删除目录下所有 .txt 文件，可根据需要修改）
#     """
#     now = datetime.now().timestamp()
#     if not os.path.exists(reports_dir):
#         return
#     for filename in os.listdir(reports_dir):
#         file_path = os.path.join(reports_dir, filename)
#         if os.path.isfile(file_path):
#             file_mtime = os.path.getmtime(file_path)
#             # 如果文件修改时间超过 keep_days 天则删除
#             if (now - file_mtime) > keep_days * 86400:
#                 os.remove(file_path)
#
# # ==================== 8. 生成 TXT 测试报告 ====================
# def generate_txt_report(results, report_path):
#     """
#     将测试结果列表写入 txt 文件
#     results: [{"id":..., "desc":..., "status":..., "error":...}, ...]
#     """
#     total = len(results)
#     passed = sum(1 for r in results if r["status"] == "PASS")
#     failed = total - passed
#     pass_rate = (passed / total * 100) if total > 0 else 0
#
#     with open(report_path, "w", encoding="utf-8") as f:
#         f.write("=" * 50 + "\n")
#         f.write(f"  测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#         f.write("=" * 50 + "\n\n")
#
#         for r in results:
#             status = r["status"]
#             line = f"[{status}] {r['id']}: {r['desc']}"
#             if r.get("error"):
#                 line += f" (错误: {r['error']})"
#             f.write(line + "\n")
#
#         f.write("\n" + "-" * 50 + "\n")
#         f.write(f"总计: {total}  通过: {passed}  失败: {failed}\n")
#         f.write(f"通过率: {pass_rate:.1f}%\n")
#         f.write("-" * 50 + "\n")






