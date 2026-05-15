#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-15 09:57
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : runner.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : 实现完整的“简易测试用例执行器”：读取 JSON 用例 → 执行（带异常捕获）→ 统计通过率 → 生成 txt 报告

import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
setup_logging,
load_json,
read_txt,
ensure_dir_os,
clean_old_reports,
generate_txt_report,
get_data_dir,
get_reports_dir
)


def fake_api_call(method, url, body):
    if body:
        if not body.get("username"):
            return 400
        if not body.get("password"):
            return 400
        return 200
    return 404

def main():
    setup_logging("INFO")
    logger = logging.getLogger(__name__)    # 根据名字返回一个 Logger 对象，用来输出日志。日志中能显示是哪个模块输出的
    #直接运行 runner.py → __name__ = "__main__"   被作为模块导入 import runner → __name__ = "runner"

    data_dir = get_data_dir()
    config = load_json(data_dir/"config.json")
    logger.info(f"配置加载完成, base_url={config["base_url"]}")

    sample_txt = read_txt(data_dir/"sample.txt")
    logger.info(f"读取到示例文本长度:{len(sample_txt)}字符")

    test_cases = load_json(data_dir/"test_cases.json")
    logger.info(f"从JSON加载了{len(test_cases)}条用例")

    reports_dir = get_reports_dir()
    ensure_dir_os(reports_dir)      # 确保有目录
    clean_old_reports(reports_dir)   #  检测清理旧报告

    results = []
    for case in test_cases:
        case_id = case["id"]   # 如果 "id" 不存在，会抛出 KeyError。适合必填字段，缺了就说明数据本身有问题，应该暴露出来。
        desc = case.get("desc", "")  #如果 "desc" 不存在，返回默认值空字符串 ""。
        method = case.get("method", "GET") #安全取值，默认 "GET"。如果用例没写 method，就当 GET 请求处理
        url = case.get("url", "")
        body = case.get("body", {})
        expected = case.get("expected_code", 200)
        #GET 是最常见的接口请求方法，而且它没有请求体，不会像 POST 那样因为缺少 body 而报错。
        # 如果用例本身漏写了 method，用 GET 去请求至少能拿到一个响应，而不会直接崩溃。
        # 200 是通用的"成功"状态码。如果用例没写预期值，假设成功总比假设失败更合理——因为一旦实际返回不是 200，
        # 断言会立刻失败提醒你，不会悄悄通过。
        # 总的来说，这两个默认值是为了让不完整的用例也能安全执行并暴露问题，而不是直接中断。

        logger.info(f"执行{case["id"]}:{desc}")

        try:
            actual = fake_api_call(method, url, body)
            if actual == expected:
                results.append({"id":case_id, "desc":desc, "status":"PASS"})
                logger.info(f" PASS(expected{expected},got{actual})")

            else:
                error_msg = f"状态码不匹配,期望{expected},实际{actual}"
                results.append({"id":case_id, "desc":desc, "status":"FAIL", "error_msg":error_msg})
                logger.error(f" FAIL-{error_msg}")

        except Exception as e:
            # 除系统异常之外的所有异常都被捕获，不影响后续用例测试
            results.append({"id":case_id, "desc":desc, "status":"ERROR", "error":str(e)})
            logger.exception(f" ERROR-用例执行异常:{e}")


    report_path = reports_dir/f"test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt"
    generate_txt_report(results, report_path)
    logger.info(f"测试报告已生成:{report_path}")

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    total = len(results)
    logger.info(f"==========执行完毕==========")
    logger.info(f"总计:{total}通过:{passed}失败:{failed}错误:{errors}")
    if total > 0:
        logger.info(f"通过率:{passed/total*100:.1f}%")



if __name__ == "__main__":
    from datetime import datetime
    main()


## runner.py - 简易测试用例执行器（完整版）
# import sys
# from pathlib import Path
# import logging
#
# # 添加当前目录到搜索路径
# sys.path.insert(0, str(Path(__file__).parent))
#
# from utils import (
#     setup_logging,
#     load_json,
#     read_txt,
#     ensure_dir_os,
#     clean_old_reports,
#     generate_txt_report,
#     get_data_dir,
#     get_reports_dir,
# )
#
# def fake_api_call(method, url, body):
#     """模拟接口调用：根据请求体内容返回状态码"""
#     if body:
#         if not body.get("username"):
#             return 400
#         if not body.get("password"):
#             return 400
#         return 200
#     return 404
#
# def main():
#     # 1. 初始化日志
#     setup_logging("INFO")
#     logger = logging.getLogger(__name__)
#
#     # 2. 加载配置和测试数据
#     data_dir = get_data_dir()
#     config = load_json(data_dir / "config.json")
#     logger.info(f"配置加载完成，base_url={config['base_url']}")
#
#     # 演示读取 txt 文件（作为模板或日志示例）
#     sample_txt = read_txt(data_dir / "sample.txt")
#     logger.info(f"读取到示例文本长度: {len(sample_txt)} 字符")
#
#     # 读取 JSON 格式的测试用例
#     test_cases = load_json(data_dir / "test_cases.json")
#     logger.info(f"从 JSON 加载了 {len(test_cases)} 条用例")
#
#     # 3. 准备报告目录（使用 os.makedirs）
#     reports_dir = get_reports_dir()
#     ensure_dir_os(reports_dir)          # 如果没有则创建
#     clean_old_reports(reports_dir)      # 清理旧报告
#
#     # 4. 执行测试用例，单个失败不影响整体
#     results = []
#     for case in test_cases:
#         case_id = case["id"]
#         desc = case.get("desc", "")
#         method = case.get("method", "GET")
#         url = case.get("url", "")
#         body = case.get("body", {})
#         expected = case.get("expected_code", 200)
#
#         logger.info(f"执行 {case_id}: {desc}")
#
#         try:
#             actual = fake_api_call(method, url, body)
#             if actual == expected:
#                 results.append({"id": case_id, "desc": desc, "status": "PASS"})
#                 logger.info(f"  PASS (expected {expected}, got {actual})")
#             else:
#                 error_msg = f"状态码不匹配，期望 {expected}，实际 {actual}"
#                 results.append({"id": case_id, "desc": desc, "status": "FAIL", "error": error_msg})
#                 logger.error(f"  FAIL - {error_msg}")
#         except Exception as e:
#             # 任何意外异常都会被捕获，不影响后续用例
#             results.append({"id": case_id, "desc": desc, "status": "ERROR", "error": str(e)})
#             logger.exception(f"  ERROR - 用例执行异常: {e}")
#
#     # 5. 生成 txt 报告
#     report_path = reports_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#     generate_txt_report(results, report_path)
#     logger.info(f"测试报告已生成：{report_path}")
#
#     # 6. 控制台输出汇总
#     passed = sum(1 for r in results if r["status"] == "PASS")
#     failed = sum(1 for r in results if r["status"] == "FAIL")
#     errors = sum(1 for r in results if r["status"] == "ERROR")
#     total = len(results)
#     logger.info(f"========== 执行完毕 ==========")
#     logger.info(f"总计: {total}, 通过: {passed}, 失败: {failed}, 错误: {errors}")
#     if total > 0:
#         logger.info(f"通过率: {passed/total*100:.1f}%")
#
# if __name__ == "__main__":
#     import datetime  # 忘了导入的话这里补一下
#     main()
