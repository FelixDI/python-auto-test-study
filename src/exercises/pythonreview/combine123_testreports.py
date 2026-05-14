#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-13 14:37
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : combine123_testreports.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 前三块的知识点汇总综合练习2 生成测试报告（字符串拼接/切片/格式化）


test_results = [
    {"id": "TC001", "desc": "正常登录", "status": "PASS", "time": 0.23},
    {"id": "TC002", "desc": "缺少密码", "status": "FAIL", "time": 0.15, "error": "excepted 400, got 200"},
    {"id": "TC003", "desc": "获取用户信息", "status": "PASS", "time": 0.08},
]

title = "自动化测试报告"
date = "2026-05-11 14:30:00"
header_line = "=" * 50
report_title = f"{header_line}\n{title}|{date}\n{header_line}"
print(report_title)

print(f"\n报告日期:{date[:10]}")

row_template = "{id:<6}{desc:<16}{status:<6}{time:>6}s{error}"   # 定义了一个字符串模版

print(f"\n{'ID':<6}{'描述':<16}{'状态':<6}{'耗时':>6} 错误信息")
print('-'*50)

pass_count = 0
fail_count = 0

for r in test_results:
    error_msg = r.get("error","")
    row = row_template.format(
        id = r["id"],
        desc = r["desc"],
        status = r["status"],
        time = r["time"],
        error = error_msg,
    )
    print(row)

    if r["status"] == "PASS":
        pass_count += 1
    else:
        fail_count += 1


summary = f"""
{'-'*50}
 总计:{len(test_results)}条
 通过:{pass_count}条({pass_count/len(test_results)*100:.1f}%)
 失败:{fail_count}条({fail_count/len(test_results)*100:.1f}%)
{'-'*50}
"""
print(summary)

sample_log = "[ERROR]2026-05-11:connection timeout"

level_start = sample_log.find("[") + 1
level_end = sample_log.find("]")
log_level = sample_log[level_start:level_end]
print(f"日志级别:{log_level}")

raw_msg = " timeout error \n"
clean_msg = raw_msg.strip()
print(f"清洗后:{clean_msg}")

footer_tpl = "报告生成于{data},由{user}生成"
footer = footer_tpl.replace("{data}", date).replace("{user}", "自动化框架")
print(footer)

# # ============================================
# # 综合练习2：字符串拼接 / 切片 / 格式化，生成测试报告
# # ============================================
#
# # ------ 模拟测试结果数据 ------
# test_results = [
#     {"id": "TC001", "desc": "正常登录", "status": "PASS", "time": 0.23},
#     {"id": "TC002", "desc": "缺少密码", "status": "FAIL", "time": 0.15, "error": "expected 400, got 200"},
#     {"id": "TC003", "desc": "获取用户信息", "status": "PASS", "time": 0.08},
# ]
#
# # ------ 1. 拼接报告头部 ------
# title = "自动化测试报告"
# date = "2026-05-11 14:30:00"
# header_line = "=" * 50                          # 重复50个=号
# report_title = f"{header_line}\n  {title}  |  {date}\n{header_line}"
# print(report_title)
#
# # ------ 2. 用切片截取时间只显示日期 ------
# print(f"\n报告日期: {date[:10]}")               # 截取前10个字符 -> 2026-05-11
#
# # ------ 3. 格式化输出每条用例 ------  # 修改此处：三引号改为单引号 -> 下文也要同步改
# row_template = "{id:<6} {desc:<16} {status:<6} {time:>6}s  {error}"  # 左对齐/右对齐
#
# # 表头
# print(f"\n{'ID':<6} {'描述':<16} {'状态':<6} {'耗时':>6}  错误信息")
# print("-" * 50)
#
# # 遍历输出
# pass_count = 0
# fail_count = 0
#
# for r in test_results:
#     error_msg = r.get("error", "")              # 无报错则空字符串
#     row = row_template.format(
#         id=r["id"],
#         desc=r["desc"],
#         status=r["status"],
#         time=r["time"],
#         error=error_msg,
#     )
#     print(row)
#
#     # 切片判断状态用于统计
#     if r["status"] == "PASS":
#         pass_count += 1
#     else:
#         fail_count += 1
#
# # ------ 4. 拼接汇总信息 ------
# summary = f"""
# {'-' * 50}
#   总计: {len(test_results)} 条
#   通过: {pass_count} 条 ({pass_count/len(test_results)*100:.1f}%)
#   失败: {fail_count} 条 ({fail_count/len(test_results)*100:.1f}%)
# {'-' * 50}
# """
# print(summary)
#
# # ------ 5. 其他字符串操作演示 ------
# sample_log = "[ERROR] 2026-05-11: connection timeout"
#
# # find + 切片提取日志级别
# level_start = sample_log.find("[") + 1
# level_end = sample_log.find("]")
# log_level = sample_log[level_start:level_end]
# print(f"日志级别: {log_level}")                 # ERROR
#
# # strip 清洗空白
# raw_msg = "   timeout error   \n"
# clean_msg = raw_msg.strip()
# print(f"清洗后: '{clean_msg}'")
#
# # replace 替换模板
# footer_tpl = "报告生成于 {date}，由 {user} 生成"
# footer = footer_tpl.replace("{date}", date).replace("{user}", "自动化框架")
# print(footer)